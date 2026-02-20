import pygame
import sys
import random

pygame.init()

# Screen setup
WIDTH, HEIGHT = 600, 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Water Filtration Simulation - Advanced")

clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 18)
big_font = pygame.font.SysFont("arial", 22, bold=True)

# Colors
WHITE = (255, 255, 255)
BLUE = (80, 150, 255)
DARK_BLUE = (60, 90, 200)
GRAY = (160, 160, 160)
YELLOW = (194, 178, 128)
BLACK = (40, 40, 40)
OUTLINE = (100, 100, 100)
RED = (200, 50, 50)
GREEN = (50, 180, 70)

# Filter settings
container_x = 200
container_width = 200
filter_top = 200
layer_height = 100

layers = [
    ("Rocks", GRAY, 0.20),     # removes 20%
    ("Sand", YELLOW, 0.30),    # removes 30%
    ("Charcoal", BLACK, 0.35), # removes 35%
    ("Cotton", WHITE, 0.15)    # removes 15%
]

# Water properties
water_y = 120
water_speed = 1.2
water_radius = 18

# Impurity system
impurity = 100  # starts 100%
particles = []

def reset_simulation():
    global water_y, impurity, particles
    water_y = 120
    impurity = 100
    particles = []
    for _ in range(30):
        particles.append([
            container_x + container_width//2 + random.randint(-10, 10),
            water_y + random.randint(-10, 10)
        ])

reset_simulation()

running = True

while running:
    clock.tick(60)
    screen.fill((235, 235, 235))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Title
    title = big_font.render("Water Filtration Simulation", True, (0, 0, 0))
    screen.blit(title, (150, 40))

    # Draw container
    pygame.draw.rect(screen, OUTLINE,
                     (container_x, filter_top,
                      container_width, layer_height*4), 3)

    # Draw layers
    for i, (name, color, _) in enumerate(layers):
        y = filter_top + i * layer_height
        pygame.draw.rect(screen, color,
                         (container_x, y,
                          container_width, layer_height))
        label = font.render(name, True, (0, 0, 0))
        screen.blit(label, (container_x - 120, y + 40))

    # Move water
    water_y += water_speed

    # Remove impurities when entering new layer
    for i, (_, _, removal_rate) in enumerate(layers):
        layer_start = filter_top + i * layer_height
        if layer_start < water_y < layer_start + 5:
            impurity -= impurity * removal_rate

            # Remove some particles visually
            remove_count = int(len(particles) * removal_rate)
            particles = particles[:-remove_count]

    # Draw water bubble
    pygame.draw.circle(screen, BLUE,
                       (container_x + container_width//2, int(water_y)),
                       water_radius)

    # Move particles with water
    for p in particles:
        p[1] = water_y + random.randint(-10, 10)
        pygame.draw.circle(screen, DARK_BLUE, (int(p[0]), int(p[1])), 3)

    # Impurity meter
    pygame.draw.rect(screen, RED, (420, 250, 30, 200))
    clean_height = 200 * (1 - impurity / 100)
    pygame.draw.rect(screen, GREEN,
                     (420, 250 + (200 - clean_height),
                      30, clean_height))

    impurity_text = font.render(f"Impurity: {impurity:.1f}%", True, (0, 0, 0))
    screen.blit(impurity_text, (390, 220))

    # Reset loop
    if water_y > filter_top + layer_height*4 + 40:
        pygame.time.delay(1000)
        reset_simulation()

    pygame.display.flip()

pygame.quit()
sys.exit()
