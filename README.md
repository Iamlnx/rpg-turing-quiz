# RPG Turing Quiz

## Objetivos

Este projeto é um jogo de RPG no formato de quiz, com temática de computabilidade e complexidade de algoritmos. O objetivo é criar uma experiência lúdica e educativa onde o jogador avança em uma narrativa de RPG ao responder perguntas relacionadas a conceitos fundamentais de computação.

## Stack

- **Python**
- **Pygame** (motor gráfico para jogos em Python)
- **FastAPI** (backend para API e integração)
- **SQLite** (banco de dados leve e prático)
- **Git & GitHub** (controle de versão e colaboração)
- **Docker** (containerização para facilitar o deploy e execução)

## Como rodar localmente

1. **Clone o repositório**
   ```bash
   git clone https://github.com/Iamlnx/rpg-turing-quiz.git
   cd rpg-turing-quiz
   ```

2. **Crie e ative um ambiente virtual (opcional, mas recomendado)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

4. **Rodando localmente com Docker**
   - Certifique-se de ter o Docker instalado.
   - Execute:
     ```bash
     docker build -t rpg-turing-quiz .
     docker run -p 8000:8000 rpg-turing-quiz
     ```

5. **Executando sem Docker**
   - Para rodar o backend FastAPI:
     ```bash
     uvicorn app.main:app --reload
     ```
   - Para rodar o jogo (interface gráfica com Pygame), execute o arquivo principal do jogo (exemplo):
     ```bash
     python game/main.py
     ```

> **Observação:** Os caminhos acima podem variar conforme a estrutura do projeto for evoluindo.

---

Sinta-se à vontade para contribuir e sugerir melhorias!
