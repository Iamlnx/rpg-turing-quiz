from database import get_connection
from questions import questions

conn = get_connection()
cur = conn.cursor()

for q in questions:
    cur.execute("""
        INSERT INTO Pergunta (enunciado, alternativa_a, alternativa_b, alternativa_c, alternativa_d, resposta_correta)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        q["question"],
        q["options"][0],
        q["options"][1],
        q["options"][2],
        q["options"][3],
        q["answer_index"]
    ))

conn.commit()
conn.close()
print("✅ Perguntas inseridas com sucesso!")
