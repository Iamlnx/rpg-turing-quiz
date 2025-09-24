import pygame
import requests
import sys

API_URL = "http://127.0.0.1:8000"

pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("A Máquina de Turing: Jornada no Reino da Computabilidade")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 100, 200)

font = pygame.font.SysFont(None, 32)

def draw_text(text, x, y, color=BLACK):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

def launch_game():

    try:
        response = requests.get(f"{API_URL}/launch")
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print("Erro ao conectar com backend:", e)
    return None

def send_score(question, answer_index):
    """Envia a resposta do jogador para o backend e devolve o resultado"""
    data = {"question": question, "answer": answer_index}
    try:
        response = requests.post(f"{API_URL}/score", json=data)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print("Erro ao enviar resposta:", e)
    return None

def main():
    clock = pygame.time.Clock()
    running = True
    question_data = launch_game() 
    selected_option = 0
    message = ""

    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(question_data["options"])
                elif event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(question_data["options"])
                elif event.key == pygame.K_RETURN:

                    result = send_score(question_data["question"], selected_option)
                    if result:
                        message = f"{result['result']} (+{result['points']} pontos)"
                        
                        question_data = launch_game()
                        selected_option = 0

        draw_text(question_data["question"], 50, 50, BLUE)

        for i, option in enumerate(question_data["options"]):
            color = BLACK
            if i == selected_option:
                color = BLUE
            draw_text(f"{i+1}. {option}", 70, 120 + i*40, color)

        draw_text(message, 50, 400, BLUE)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
