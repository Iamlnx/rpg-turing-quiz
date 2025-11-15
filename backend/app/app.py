# backend/app/app.py
from flask import Flask, jsonify, request
import os
import random
from game.database import get_connection, init_db
# tentamos importar as perguntas do módulo game.questions
try:
    from game.questions import questions as QUESTIONS
except Exception:
    # fallback: lista mínima caso não exista game.questions
    QUESTIONS = [
        {
            "question": "O que é a Máquina de Turing?",
            "options": [
                "Um modelo teórico de computação",
                "Um tipo de robô",
                "Uma linguagem de programação",
                "Um processador"
            ],
            "answer_index": 0
        },
        {
            "question": "Qual estrutura de dados usa FIFO?",
            "options": ["Pilha", "Fila", "Árvore", "Grafo"],
            "answer_index": 1
        }
    ]

app = Flask(__name__)

# TOKEN FIXO (tarefa 2)
# formato esperado no header Authorization: "Bearer <TOKEN>"
AUTH_TOKEN = "123456"

# ---------------------------
# Inicializa DB e faz seed automático
# ---------------------------
def ensure_db_and_seed():
    init_db()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) as cnt FROM Pergunta")
    row = cur.fetchone()
    count = row["cnt"] if row else 0

    if count == 0:
        for q in QUESTIONS:
            options = q.get("options", [])
            a = options[0] if len(options) > 0 else None
            b = options[1] if len(options) > 1 else None
            c = options[2] if len(options) > 2 else None
            d = options[3] if len(options) > 3 else None
            answer = q.get("answer_index", 0)
            cur.execute("""
                INSERT INTO Pergunta (enunciado, alternativa_a, alternativa_b, alternativa_c, alternativa_d, resposta_correta)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (q.get("question"), a, b, c, d, answer))
        conn.commit()
        print("✅ Seed de perguntas executado (inseridas perguntas).")
    conn.close()

ensure_db_and_seed()

# ---------------------------
# Helper de autenticação
# ---------------------------
def check_auth_header():
    """Retorna True se header Authorization contém 'Bearer <AUTH_TOKEN>'"""
    auth = request.headers.get("Authorization", "")
    if not auth:
        return False
    parts = auth.split()
    if len(parts) == 2 and parts[0].lower() == "bearer" and parts[1] == AUTH_TOKEN:
        return True
    return False

# Nós liberamos /health sem token
@app.before_request
def require_token():
    if request.path == "/health":
        return None
    # permitir OPTIONS para CORS/preflight
    if request.method == "OPTIONS":
        return None
    if not check_auth_header():
        return jsonify({"error": "Unauthorized"}), 401

# ---------------------------
# Health check (livre)
# ---------------------------
@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok"}), 200

# ---------------------------
# /launch - criar partida e retornar pergunta aleatória
# ---------------------------
@app.route("/launch", methods=["GET"])
def launch():
    player_name = request.args.get("nome", "").strip()
    if not player_name:
        return jsonify({"error": "Parâmetro 'nome' é obrigatório"}), 400

    conn = get_connection()
    cur = conn.cursor()

    # verifica/extrai jogador
    cur.execute("SELECT id_jogador FROM Jogador WHERE nome = ?", (player_name,))
    jogador = cur.fetchone()
    if jogador:
        id_jogador = jogador["id_jogador"]
    else:
        cur.execute("INSERT INTO Jogador (nome) VALUES (?)", (player_name,))
        id_jogador = cur.lastrowid

    # cria partida
    cur.execute("INSERT INTO Partida (id_jogador) VALUES (?)", (id_jogador,))
    id_partida = cur.lastrowid
    conn.commit()

    # pega pergunta aleatória
    cur.execute("SELECT * FROM Pergunta ORDER BY RANDOM() LIMIT 1")
    q = cur.fetchone()
    conn.close()

    if not q:
        return jsonify({"error": "Nenhuma pergunta encontrada no banco"}), 500

    return jsonify({
        "id_partida": id_partida,
        "id_pergunta": q["id_pergunta"],
        "question": q["enunciado"],
        "options": [
            q["alternativa_a"],
            q["alternativa_b"],
            q["alternativa_c"],
            q["alternativa_d"]
        ],
        "player_name": player_name,
        "id_jogador": id_jogador
    }), 200

# ---------------------------
# /score - receber resposta, gravar e retornar resultado/pontos
# ---------------------------
@app.route("/score", methods=["POST"])
def score():
    data = request.json or {}
    id_partida = data.get("id_partida")
    id_pergunta = data.get("id_pergunta")
    answer = data.get("answer")

    if id_partida is None or id_pergunta is None or answer is None:
        return jsonify({"error": "Campos obrigatórios: id_partida, id_pergunta, answer"}), 400

    conn = get_connection()
    cur = conn.cursor()

    # verificar existência da pergunta
    cur.execute("SELECT resposta_correta FROM Pergunta WHERE id_pergunta = ?", (id_pergunta,))
    row = cur.fetchone()
    if not row:
        conn.close()
        return jsonify({"error": "Pergunta não encontrada"}), 404

    correta = (row["resposta_correta"] == answer)
    pontos = 10 if correta else 0

    try:
        cur.execute("""
            INSERT INTO Resposta (id_partida, id_pergunta, resposta_jogador, correta)
            VALUES (?, ?, ?, ?)
        """, (id_partida, id_pergunta, answer, int(correta)))

        cur.execute("""
            UPDATE Partida
            SET pontuacao_total = pontuacao_total + ?
            WHERE id_partida = ?
        """, (pontos, id_partida))

        conn.commit()
    except Exception as e:
        conn.rollback()
        conn.close()
        return jsonify({"error": "Erro ao gravar no banco", "detail": str(e)}), 500

    conn.close()
    return jsonify({"result": "Correto!" if correta else "Errado!", "points": pontos}), 200

# ---------------------------
# /results - ranking geral
# ---------------------------
@app.route("/results", methods=["GET"])
def results():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            j.nome AS nome,
            COALESCE(SUM(p.pontuacao_total), 0) AS total_pontos,
            COUNT(p.id_partida) AS partidas_jogadas,
            MAX(p.data_inicio) AS ultima_partida
        FROM Jogador j
        LEFT JOIN Partida p ON j.id_jogador = p.id_jogador
        GROUP BY j.id_jogador
        ORDER BY total_pontos DESC
    """)
    ranking = [dict(row) for row in cur.fetchall()]
    conn.close()
    return jsonify(ranking), 200

if __name__ == "__main__":
    # Execute a partir da raiz: python backend\app\app.py
    app.run(debug=True, host="0.0.0.0", port=8000)
