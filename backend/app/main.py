from flask import Flask, jsonify, request
import random

from game.questions import questions

app = Flask(__name__)

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok"})

@app.route("/launch", methods=["GET"])
def launch():
    q = random.choice(questions)
    return jsonify({
        "question": q["question"],
        "options": q["options"]
    })

@app.route("/score", methods=["POST"])
def score():
    data = request.json
    question = data.get("question")
    answer = data.get("answer")

    for q in questions:
        if q["question"] == question:
            if answer == q["answer_index"]:
                return jsonify({"result": "Correto!", "points": 10})
            else:
                return jsonify({"result": "Errado!", "points": 0})

    return jsonify({"result": "Pergunta não encontrada", "points": 0})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
