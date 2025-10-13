from flask import Flask, jsonify, request
import random
import sqlite3
from game.database import get_connection
import os

app = Flask(__name__)

# ---------------------------
# Health check
# ---------------------------
@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok"})

# ---------------------------
# Inicia uma partida nova
# ---------------------------
@app.route("/launch", methods=["GET"])
def launch():
    conn = get_connection()
    cur = conn.cursor()

    # Captura o nome do jogador enviado pela query string
    player_name = request.args.get("nome", "Jogador1").strip()

    # Verifica se jogador já existe
    cur.execute("SELECT id_jogador FROM Jogador WHERE nome = ?", (player_name,))
    jogador = cur.fetchone()

    if jogador:
        id_jogador = jogador["id_jogador"]
    else:
        cur.execute("INSERT INTO Jogador (nome) VALUES (?)", (player_name,))
        id_jogador = cur.lastrowid

    # Cria nova partida vinculada ao jogador
    cur.execute("INSERT INTO Partida (id_jogador) VALUES (?)", (id_jogador,))
    id_partida = cur.lastrowid

    # 🔥 Commit ANTES de buscar a pergunta e fechar
    conn.commit()

    # Busca uma pergunta aleatória
    cur.execute("SELECT * FROM Pergunta ORDER BY RANDOM() LIMIT 1")
    q = cur.fetchone()

    conn.close()

    if not q:
        return jsonify({"error": "Nenhuma pergunta encontrada no banco"}), 400

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
    })


# ---------------------------
# Recebe a resposta do jogador e grava no banco
# ---------------------------
@app.route("/score", methods=["POST"])
def score():
    data = request.json
    id_partida = data.get("id_partida")
    id_pergunta = data.get("id_pergunta")
    answer_index = data.get("answer")

    conn = get_connection()
    cur = conn.cursor()

    # Buscar resposta correta da pergunta
    cur.execute("SELECT resposta_correta FROM Pergunta WHERE id_pergunta = ?", (id_pergunta,))
    row = cur.fetchone()

    if not row:
        conn.close()
        return jsonify({"result": "Pergunta não encontrada", "points": 0})

    correta = row["resposta_correta"] == answer_index
    pontos = 10 if correta else 0

    # Registrar resposta do jogador
    cur.execute("""
        INSERT INTO Resposta (id_partida, id_pergunta, resposta_jogador, correta)
        VALUES (?, ?, ?, ?)
    """, (id_partida, id_pergunta, answer_index, correta))

    # Atualizar pontuação total da partida
    cur.execute("""
        UPDATE Partida
        SET pontuacao_total = pontuacao_total + ?
        WHERE id_partida = ?
    """, (pontos, id_partida))

    conn.commit()
    conn.close()

    return jsonify({
        "result": "Correto!" if correta else "Errado!",
        "points": pontos
    })


# ---------------------------
# Exibe os resultados da partida (consulta)
# ---------------------------
# ---------------------------
# Exibe ranking geral por jogador (agrupado)
# ---------------------------
@app.route("/results", methods=["GET"])
def results():
    conn = get_connection()
    cur = conn.cursor()

    # Agrupa a pontuação total por jogador
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

    return jsonify(ranking)



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
