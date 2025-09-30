# RPG Turing Quiz

## Objetivos

Este projeto é um jogo de RPG no formato de quiz, com temática de computabilidade e complexidade de algoritmos. O objetivo é criar uma experiência lúdica e educativa onde o jogador avança em uma narrativa de RPG ao responder perguntas relacionadas a conceitos fundamentais de computação.

## Stack

- **Python**
- **Pygame** (motor gráfico para jogos em Python)
- **Flask** (backend simples para API e integração)
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
         cd backend
      python app.py

      O backend estará disponível em: http://127.0.0.1:8000

      Rotas disponíveis:
      - GET `/health` → checa se o servidor está ativo
      - GET `/launch` → cria partida/sessão
      - POST `/score` → envia e registra pontuação

6. **Executando o jogo**
      cd ../game
      python main.py

      ** Observação: O backend precisa estar rodando antes de iniciar o jogo.



---

Sinta-se à vontade para contribuir e sugerir melhorias!
