import pygame
import random
import sys
import uuid

# Initialize pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 600, 600
CELL_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man Clone")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

# Session to identify player
player_id = str(uuid.uuid4())
print(f"Player ID: {player_id}")

# Set up player and ghosts
player_pos = [WIDTH // 2, HEIGHT // 2]
ghosts = [[random.randint(0, WIDTH // CELL_SIZE - 1) * CELL_SIZE,
           random.randint(0, HEIGHT // CELL_SIZE - 1) * CELL_SIZE]]

# Set up points
points = []
for i in range(50):
    points.append([random.randint(0, WIDTH // CELL_SIZE - 1) * CELL_SIZE,
                   random.randint(0, HEIGHT // CELL_SIZE - 1) * CELL_SIZE])

# Player movement speed
speed = CELL_SIZE

# Ghost movement speed
ghost_speed = CELL_SIZE

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Score and stage
score = 0
stage = 1

# Game state
menu = True
game_over = False
pause = False

def draw_player(position):
    pygame.draw.rect(screen, YELLOW, (position[0], position[1], CELL_SIZE, CELL_SIZE))

def draw_ghost(position):
    pygame.draw.rect(screen, RED, (position[0], position[1], CELL_SIZE, CELL_SIZE))

def draw_points(points):
    for point in points:
        pygame.draw.circle(screen, WHITE, (point[0] + CELL_SIZE // 2, point[1] + CELL_SIZE // 2), 5)

def draw_menu():
    font = pygame.font.Font(None, 74)
    text = font.render("Pac-Man Clone", True, WHITE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 100))
    text = font.render("Press Enter to Start", True, WHITE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))

def draw_pause_menu():
    font = pygame.font.Font(None, 74)
    text = font.render("Paused", True, WHITE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 100))
    text = font.render("Press Enter to Resume", True, WHITE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
    text = font.render("Press Q to Quit", True, WHITE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 + 100))

def draw_game_over():
    font = pygame.font.Font(None, 74)
    text = font.render("Game Over", True, RED)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 100))
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
    text = font.render("Press Enter to Restart", True, WHITE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 + 100))

# Game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if menu and event.key == pygame.K_RETURN:
                menu = False
                game_over = False
                score = 0
                stage = 1
                player_pos = [WIDTH // 2, HEIGHT // 2]
                ghosts = [[random.randint(0, WIDTH // CELL_SIZE - 1) * CELL_SIZE,
                           random.randint(0, HEIGHT // CELL_SIZE - 1) * CELL_SIZE]]
                points = [[random.randint(0, WIDTH // CELL_SIZE - 1) * CELL_SIZE,
                           random.randint(0, HEIGHT // CELL_SIZE - 1) * CELL_SIZE] for _ in range(50)]
            elif game_over and event.key == pygame.K_RETURN:
                menu = True
            elif event.key == pygame.K_ESCAPE:
                if not menu and not game_over:
                    pause = not pause
            elif pause and event.key == pygame.K_RETURN:
                pause = False
            elif pause and event.key == pygame.K_q:
                pygame.quit()
                sys.exit()

    if menu:
        screen.fill(BLACK)
        draw_menu()
        pygame.display.flip()
        continue

    if pause:
        screen.fill(BLACK)
        draw_pause_menu()
        pygame.display.flip()
        continue

    # Handle player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_pos[0] -= speed
    if keys[pygame.K_RIGHT]:
        player_pos[0] += speed
    if keys[pygame.K_UP]:
        player_pos[1] -= speed
    if keys[pygame.K_DOWN]:
        player_pos[1] += speed

    # Keep player on screen
    player_pos[0] = player_pos[0] % WIDTH
    player_pos[1] = player_pos[1] % HEIGHT

    # Ghost movement (basic random movement)
    for ghost_pos in ghosts:
        ghost_pos[0] += random.choice([-ghost_speed, 0, ghost_speed])
        ghost_pos[1] += random.choice([-ghost_speed, 0, ghost_speed])

        # Keep ghost on screen
        ghost_pos[0] = ghost_pos[0] % WIDTH
        ghost_pos[1] = ghost_pos[1] % HEIGHT

    # Check for collision with points
    for point in points[:]:
        if player_pos[0] == point[0] and player_pos[1] == point[1]:
            points.remove(point)
            score += 10

    # Check if all points are collected
    if not points:
        stage += 1
        points = [[random.randint(0, WIDTH // CELL_SIZE - 1) * CELL_SIZE,
                   random.randint(0, HEIGHT // CELL_SIZE - 1) * CELL_SIZE] for _ in range(50 + stage * 10)]
        ghost_speed += CELL_SIZE // 4  # Increase ghost speed every stage
        if stage % 2 == 0:
            # Add a new ghost every 2 stages
            ghosts.append([random.randint(0, WIDTH // CELL_SIZE - 1) * CELL_SIZE,
                           random.randint(0, HEIGHT // CELL_SIZE - 1) * CELL_SIZE])

    # Check for collision with ghosts
    for ghost_pos in ghosts:
        if player_pos[0] == ghost_pos[0] and player_pos[1] == ghost_pos[1]:
            game_over = True
            menu = True
            break

    # Draw everything
    screen.fill(BLACK)
    draw_player(player_pos)
    for ghost_pos in ghosts:
        draw_ghost(ghost_pos)
    draw_points(points)

    # Draw score
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    stage_text = font.render(f"Stage: {stage}", True, WHITE)
    screen.blit(stage_text, (WIDTH - 150, 10))

    if game_over:
        draw_game_over()

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(10)