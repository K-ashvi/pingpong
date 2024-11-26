import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
PURPLE = (138, 43, 226)
HOT_PINK = (255, 20, 147)
BLACK = (0, 0, 0)
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
BALL_RADIUS = 10
FPS = 60
FONT = pygame.font.Font(None, 74)

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong")

# Game variables
paddle1_y = HEIGHT // 2 - PADDLE_HEIGHT // 2
paddle2_y = HEIGHT // 2 - PADDLE_HEIGHT // 2
paddle_speed = 7

ball_x, ball_y = WIDTH // 2, HEIGHT // 2
ball_speed_x, ball_speed_y = 5, 5

# Score variables
score1 = 0
score2 = 0
winning_score = 5

# Clock
clock = pygame.time.Clock()

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Input handling
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and paddle1_y > 0:
        paddle1_y -= paddle_speed
    if keys[pygame.K_s] and paddle1_y < HEIGHT - PADDLE_HEIGHT:
        paddle1_y += paddle_speed
    if keys[pygame.K_UP] and paddle2_y > 0:
        paddle2_y -= paddle_speed
    if keys[pygame.K_DOWN] and paddle2_y < HEIGHT - PADDLE_HEIGHT:
        paddle2_y += paddle_speed

    # Ball movement
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Ball collision with top and bottom
    if ball_y - BALL_RADIUS <= 0 or ball_y + BALL_RADIUS >= HEIGHT:
        ball_speed_y *= -1

    # Ball collision with paddles
    if (
        ball_x - BALL_RADIUS <= PADDLE_WIDTH
        and paddle1_y < ball_y < paddle1_y + PADDLE_HEIGHT
    ) or (
        ball_x + BALL_RADIUS >= WIDTH - PADDLE_WIDTH
        and paddle2_y < ball_y < paddle2_y + PADDLE_HEIGHT
    ):
        ball_speed_x *= -1

    # Ball reset if out of bounds and update score
    if ball_x < 0:
        score2 += 1
        ball_x, ball_y = WIDTH // 2, HEIGHT // 2
        ball_speed_x *= -1
    elif ball_x > WIDTH:
        score1 += 1
        ball_x, ball_y = WIDTH // 2, HEIGHT // 2
        ball_speed_x *= -1

    # Check for winner
    if score1 == winning_score or score2 == winning_score:
        winner_text = f"Player {'1' if score1 == winning_score else '2'} Wins!"
        winner_surface = FONT.render(winner_text, True, HOT_PINK)
        screen.fill(BLACK)
        screen.blit(
            winner_surface, (WIDTH // 2 - winner_surface.get_width() // 2, HEIGHT // 2 - winner_surface.get_height() // 2)
        )
        pygame.display.flip()
        pygame.time.wait(3000)
        pygame.quit()
        sys.exit()

    # Drawing
    screen.fill(BLACK)  # Purple background

    # Draw middle line
    for y in range(0, HEIGHT, 20):
        pygame.draw.rect(screen, PURPLE, (WIDTH // 2 - 2, y, 4, 10))

    # Draw paddles and ball
    pygame.draw.rect(screen, HOT_PINK, (0, paddle1_y, PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.rect(screen, HOT_PINK, (WIDTH - PADDLE_WIDTH, paddle2_y, PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.circle(screen, HOT_PINK, (ball_x, ball_y), BALL_RADIUS)

    # Draw scores
    score1_surface = FONT.render(str(score1), True, PURPLE)
    score2_surface = FONT.render(str(score2), True, PURPLE)
    screen.blit(score1_surface, (WIDTH // 4 - score1_surface.get_width() // 2, 20))
    screen.blit(score2_surface, (3 * WIDTH // 4 - score2_surface.get_width() // 2, 20))

    pygame.display.flip()

    # Limit frame rate
    clock.tick(FPS)
