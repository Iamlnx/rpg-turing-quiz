import sqlite3
import os

# Caminho absoluto para o arquivo quiz.db dentro da pasta "game"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "quiz.db")

def get_connection():
    """Cria e retorna uma conexão com o banco de dados quiz.db"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Cria todas as tabelas do banco de dados (caso não existam)"""
    conn = get_connection()
    cur = conn.cursor()

    # Criação das tabelas
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Jogador (
        id_jogador INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS Partida (
        id_partida INTEGER PRIMARY KEY AUTOINCREMENT,
        id_jogador INTEGER,
        data_inicio DATETIME DEFAULT CURRENT_TIMESTAMP,
        data_fim DATETIME,
        pontuacao_total INTEGER DEFAULT 0,
        FOREIGN KEY (id_jogador) REFERENCES Jogador(id_jogador)
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS Pergunta (
        id_pergunta INTEGER PRIMARY KEY AUTOINCREMENT,
        enunciado TEXT NOT NULL,
        alternativa_a TEXT,
        alternativa_b TEXT,
        alternativa_c TEXT,
        alternativa_d TEXT,
        resposta_correta INTEGER
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS Resposta (
        id_resposta INTEGER PRIMARY KEY AUTOINCREMENT,
        id_partida INTEGER,
        id_pergunta INTEGER,
        resposta_jogador INTEGER,
        correta BOOLEAN,
        FOREIGN KEY (id_partida) REFERENCES Partida(id_partida),
        FOREIGN KEY (id_pergunta) REFERENCES Pergunta(id_pergunta)
    )
    """)

    conn.commit()
    conn.close()
