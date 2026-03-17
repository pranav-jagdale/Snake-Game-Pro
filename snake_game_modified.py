import pygame
import random
import sys
import os

pygame.init()
pygame.mixer.init()

# 🔥 Bigger Screen
WIDTH, HEIGHT = 900, 600
CELL = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game Pro 🐍")

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 120, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

clock = pygame.time.Clock()

HIGHSCORE_FILE = "highscore.txt"

def load_highscore():
    if os.path.exists(HIGHSCORE_FILE):
        return int(open(HIGHSCORE_FILE).read() or 0)
    return 0

def save_highscore(score):
    with open(HIGHSCORE_FILE, "w") as f:
        f.write(str(score))

# Sounds
try:
    eat_sound = pygame.mixer.Sound("eat.wav")
    gameover_sound = pygame.mixer.Sound("gameover.wav")
except:
    eat_sound = None
    gameover_sound = None

def draw_text(text, size, color, x, y):
    font = pygame.font.SysFont(None, size)
    surface = font.render(text, True, color)
    rect = surface.get_rect(center=(x, y))
    screen.blit(surface, rect)

def ai_move(head, food, direction):
    if head[0] < food[0] and direction != "LEFT":
        return "RIGHT"
    if head[0] > food[0] and direction != "RIGHT":
        return "LEFT"
    if head[1] < food[1] and direction != "UP":
        return "DOWN"
    if head[1] > food[1] and direction != "DOWN":
        return "UP"
    return direction

def spawn_food(snake):
    while True:
        pos = [random.randrange(0, WIDTH, CELL), random.randrange(0, HEIGHT, CELL)]
        if pos not in snake:
            return pos

def reset_game():
    snake = [[200, 100], [180, 100], [160, 100]]
    direction = "RIGHT"
    food = spawn_food(snake)
    score = 0
    return snake, direction, food, score

def main():
    highscore = load_highscore()

    snake, direction, food, score = reset_game()
    paused = False
    menu = True
    ai_mode = False

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if menu:
                    if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        menu = False

                else:
                    if event.key == pygame.K_p:
                        paused = not paused

                    if event.key == pygame.K_r:
                        snake, direction, food, score = reset_game()
                        paused = False

                    if event.key == pygame.K_m:
                        menu = True
                        snake, direction, food, score = reset_game()

                    if event.key == pygame.K_a:
                        ai_mode = not ai_mode

                    if not paused and not ai_mode:
                        if event.key == pygame.K_UP and direction != "DOWN":
                            direction = "UP"
                        elif event.key == pygame.K_DOWN and direction != "UP":
                            direction = "DOWN"
                        elif event.key == pygame.K_LEFT and direction != "RIGHT":
                            direction = "LEFT"
                        elif event.key == pygame.K_RIGHT and direction != "LEFT":
                            direction = "RIGHT"

        # MENU
        if menu:
            screen.fill(BLACK)
            draw_text("SNAKE GAME", 80, GREEN, WIDTH//2, HEIGHT//3)
            draw_text("ENTER to Start", 40, WHITE, WIDTH//2, HEIGHT//2)
            draw_text("A = Toggle AI", 30, WHITE, WIDTH//2, HEIGHT//2 + 50)
            draw_text(f"High Score: {highscore}", 35, RED, WIDTH//2, HEIGHT - 80)
            pygame.display.update()
            continue

        if paused:
            draw_text("PAUSED", 80, WHITE, WIDTH//2, HEIGHT//2)
            pygame.display.update()
            continue

        # AI
        if ai_mode:
            direction = ai_move(snake[0], food, direction)

        # Move
        head = snake[0][:]
        if direction == "UP":
            head[1] -= CELL
        elif direction == "DOWN":
            head[1] += CELL
        elif direction == "LEFT":
            head[0] -= CELL
        elif direction == "RIGHT":
            head[0] += CELL

        snake.insert(0, head)

        if head == food:
            score += 1
            food = spawn_food(snake)
            if eat_sound:
                eat_sound.play()
        else:
            snake.pop()

        # Collision
        if (head[0] < 0 or head[0] >= WIDTH or
            head[1] < 0 or head[1] >= HEIGHT or
            head in snake[1:]):

            if score > highscore:
                highscore = score
                save_highscore(highscore)

            if gameover_sound:
                gameover_sound.play()

            while True:
                screen.fill(BLACK)
                draw_text("GAME OVER", 80, RED, WIDTH//2, HEIGHT//3)
                draw_text(f"Score: {score}", 40, WHITE, WIDTH//2, HEIGHT//2)
                draw_text("R = Restart", 30, WHITE, WIDTH//2, HEIGHT//2 + 50)
                draw_text("M = Menu", 30, YELLOW, WIDTH//2, HEIGHT//2 + 90)

                pygame.display.update()

                for ev in pygame.event.get():
                    if ev.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if ev.type == pygame.KEYDOWN:
                        if ev.key == pygame.K_r:
                            snake, direction, food, score = reset_game()
                            break
                        if ev.key == pygame.K_m:
                            menu = True
                            snake, direction, food, score = reset_game()
                            break
                else:
                    continue
                break

        # Draw
        screen.fill(BLACK)

        # Grid
        for x in range(0, WIDTH, CELL):
            pygame.draw.line(screen, (40, 40, 40), (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, CELL):
            pygame.draw.line(screen, (40, 40, 40), (0, y), (WIDTH, y))

        # Snake
        for i, block in enumerate(snake):
            rect = pygame.Rect(block[0], block[1], CELL, CELL)
            pygame.draw.rect(screen, GREEN if i else (0,255,0), rect)
            pygame.draw.rect(screen, DARK_GREEN, rect, 2)

        # Food
        pygame.draw.rect(screen, RED, pygame.Rect(food[0], food[1], CELL, CELL))

        # HUD
        draw_text(f"Score: {score}", 30, WHITE, 100, 30)
        draw_text(f"High: {highscore}", 30, WHITE, WIDTH-100, 30)

        if ai_mode:
            draw_text("AI: ON", 25, YELLOW, WIDTH//2, 30)

        pygame.display.update()

        clock.tick(min(25, 10 + score // 5))

if __name__ == "__main__":
    main()