import pygame
import requests
import sys

API_URL = "http://127.0.0.1:8000"
AUTH_TOKEN = "123456"  # igual ao app.py

pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("A Máquina de Turing: Jornada no Reino da Computabilidade")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 100, 200)
GRAY = (200, 200, 200)

font = pygame.font.SysFont(None, 32)
big_font = pygame.font.SysFont(None, 48)

def draw_text(text, x, y, color=BLACK, font_obj=font):
    img = font_obj.render(text, True, color)
    screen.blit(img, (x, y))

def wrap_text(text, x, y, max_width=700, line_height=30, color=BLACK):
    words = text.split(" ")
    line = ""
    for word in words:
        test_line = f"{line} {word}".strip()
        if font.size(test_line)[0] > max_width:
            draw_text(line, x, y, color)
            y += line_height
            line = word
        else:
            line = test_line
    draw_text(line, x, y, color)

def launch_game(player_name):
    headers = {"Authorization": f"Bearer {AUTH_TOKEN}"}
    params = {"nome": player_name}
    try:
        response = requests.get(f"{API_URL}/launch", params=params, headers=headers, timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            print("Erro /launch:", response.status_code, response.text)
    except Exception as e:
        print("Erro ao conectar com backend:", e)
    return None

def send_score(id_partida, id_pergunta, answer_index):
    headers = {"Authorization": f"Bearer {AUTH_TOKEN}"}
    data = {
        "id_partida": id_partida,
        "id_pergunta": id_pergunta,
        "answer": answer_index
    }
    try:
        response = requests.post(f"{API_URL}/score", json=data, headers=headers, timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            print("Erro /score:", response.status_code, response.text)
    except Exception as e:
        print("Erro ao enviar resposta:", e)
    return None

def get_results():
    headers = {"Authorization": f"Bearer {AUTH_TOKEN}"}
    try:
        response = requests.get(f"{API_URL}/results", headers=headers, timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            print("Erro /results:", response.status_code, response.text)
    except Exception as e:
        print("Erro ao buscar resultados:", e)
    return []

# Resto do loop do jogo (mantive seu código original para interface)
def main():
    clock = pygame.time.Clock()
    running = True
    state = "input_name"
    player_name = ""
    total_score = 0
    question_data = None
    selected_option = 0
    message = ""
    question_count = 0
    max_questions = 5
    results_data = []

    while running:
        screen.fill(WHITE)

        if state == "input_name":
            draw_text("Digite seu nome:", 200, 200, BLUE, big_font)
            draw_text(player_name + "|", 220, 260, BLACK, big_font)
            draw_text("Pressione ENTER para começar", 180, 340, GRAY, font)
            draw_text("Pressione R para ver resultados", 200, 380, GRAY, font)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and player_name.strip():
                        question_data = launch_game(player_name.strip())
                        if question_data:
                            state = "playing"
                            question_count = 1
                            selected_option = 0
                            total_score = 0
                            message = ""
                    elif event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                    elif event.key == pygame.K_r:
                        results_data = get_results()
                        state = "results"
                    else:
                        if len(player_name) < 20 and event.unicode.isprintable():
                            player_name += event.unicode

        elif state == "playing":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        selected_option = (selected_option + 1) % len(question_data["options"])
                    elif event.key == pygame.K_UP:
                        selected_option = (selected_option - 1) % len(question_data["options"])
                    elif event.key == pygame.K_RETURN:
                        result = send_score(
                            question_data["id_partida"],
                            question_data["id_pergunta"],
                            selected_option
                        )
                        if result:
                            total_score += result.get("points", 0)
                            message = f"{result.get('result','')} (+{result.get('points',0)} pts)"

                            question_count += 1
                            if question_count > max_questions:
                                state = "finished"
                                continue

                            question_data = launch_game(player_name)
                            selected_option = 0
                    elif event.key == pygame.K_r:
                        results_data = get_results()
                        state = "results"

            if question_data:
                draw_text(f"Pergunta {question_count}/{max_questions}", 50, 20, GRAY)
                wrap_text(question_data["question"], 50, 70, max_width=700, line_height=28, color=BLUE)

                for i, option in enumerate(question_data["options"]):
                    color = BLUE if i == selected_option else BLACK
                    wrap_text(f"{i+1}. {option}", 70, 180 + i*60, max_width=700, line_height=28, color=color)

                draw_text(message, 50, 450, BLUE)
                draw_text(f"Pontuação: {total_score}", 50, 520, GRAY)
                draw_text("Pressione R para ver resultados", 500, 20, GRAY)

        elif state == "results":
            draw_text("🏆 Ranking Geral", 260, 50, BLUE, big_font)
            y = 120

            if not results_data:
                draw_text("Nenhum resultado encontrado.", 250, 200, BLACK)
            else:
                for row in results_data:
                    nome = row.get("nome", "Desconhecido")
                    pontos = row.get("total_pontos", 0)
                    partidas = row.get("partidas_jogadas", 0)
                    ultima = row.get("ultima_partida", "") or "—"

                    draw_text(f"{nome:<15} | Pontos: {pontos} | Partidas: {partidas} | Última: {ultima[:10]}", 80, y, BLACK)
                    y += 40
                    if y > 500:
                        break

            draw_text("Pressione ENTER para voltar", 250, 540, GRAY)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        state = "input_name"

        elif state == "finished":
            draw_text(f"🏁 Fim de jogo, {player_name}!", 200, 200, BLUE, big_font)
            draw_text(f"Sua pontuação final: {total_score} pontos", 180, 260, BLACK, big_font)
            draw_text("Pressione ENTER para nova partida", 200, 340, GRAY)
            draw_text("Pressione ESC para sair", 260, 380, GRAY)
            draw_text("Pressione R para ver resultados", 240, 420, GRAY)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_RETURN:
                        state = "input_name"
                        player_name = ""
                    elif event.key == pygame.K_r:
                        results_data = get_results()
                        state = "results"

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
