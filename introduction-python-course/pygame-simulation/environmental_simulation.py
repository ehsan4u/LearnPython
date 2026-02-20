import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 1300, 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Environmental Digital Twin Simulator")

clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 16)
big_font = pygame.font.SysFont("arial", 22, bold=True)

# COLORS
BLUE = (70, 140, 255)
DARK_BLUE = (30, 70, 200)
RED = (200, 50, 50)
GREEN = (50, 180, 70)
GRAY = (150, 150, 150)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHT_GRAY = (230, 230, 230)

# ENVIRONMENT VARIABLES
river_pollution = 50
sea_pollution = 30
fish_population = 120
tank_level = 0
field_health = 50
temperature = 25
rain = False

# SYSTEM SETTINGS
pollution_rate = 0.3
treatment_efficiency = 0.6
ai_mode = False
treatment_cost = 0
environmental_damage_cost = 0

pollution_history = []
fish_history = []

frame_count = 0

running = True

while running:
    clock.tick(60)
    screen.fill(LIGHT_GRAY)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                ai_mode = not ai_mode
            if event.key == pygame.K_UP:
                pollution_rate += 0.1
            if event.key == pygame.K_DOWN:
                pollution_rate = max(0, pollution_rate - 0.1)

    # ---------- FACTORIES ----------
    factories = 3
    river_pollution += factories * pollution_rate

    # ---------- CLIMATE ----------
    if frame_count % 800 == 0:
        rain = random.choice([True, False])

    if rain:
        river_pollution -= 0.4

    evaporation = (temperature - 20) * 0.03
    river_pollution += evaporation

    # ---------- AI OPTIMIZATION ----------
    if ai_mode:
        if river_pollution > 70:
            treatment_efficiency = 0.9
        elif river_pollution > 40:
            treatment_efficiency = 0.7
        else:
            treatment_efficiency = 0.5

    # ---------- TREATMENT ----------
    cleaned = river_pollution * treatment_efficiency * 0.02
    river_pollution -= cleaned
    tank_level += cleaned * 3
    treatment_cost += treatment_efficiency * 2

    # ---------- IRRIGATION ----------
    if tank_level > 15:
        field_health += 0.2
        tank_level -= 8

    # ---------- SEA FLOW ----------
    sea_pollution += river_pollution * 0.01

    # ---------- ECOSYSTEM ----------
    if river_pollution > 75:
        fish_population -= 0.5
        environmental_damage_cost += 3
    elif river_pollution < 40:
        fish_population += 0.3

    # BOUNDS
    river_pollution = max(0, min(100, river_pollution))
    fish_population = max(0, min(200, fish_population))
    field_health = max(0, min(100, field_health))

    # HISTORY
    if frame_count % 10 == 0:
        pollution_history.append(river_pollution)
        fish_history.append(fish_population)
        if len(pollution_history) > 250:
            pollution_history.pop(0)
            fish_history.pop(0)

    # ---------- DRAW RIVER ----------
    river_color = (70, max(0, 200 - int(river_pollution*2)), 255)
    pygame.draw.rect(screen, river_color, (0, 420, WIDTH, 120))
    screen.blit(font.render("River", True, BLACK), (10, 390))

    # ---------- DRAW SEA ----------
    sea_color = (30, max(0, 150 - int(sea_pollution*2)), 200)
    pygame.draw.rect(screen, sea_color, (950, 420, 350, 200))
    screen.blit(font.render("Sea", True, WHITE), (1080, 390))

    # ---------- FACTORY ZONE ----------
    for i in range(factories):
        pygame.draw.rect(screen, GRAY, (80 + i*120, 260, 80, 100))
    screen.blit(font.render("Industrial Zone (3 Factories)", True, BLACK), (80, 230))

    # ---------- TREATMENT ----------
    pygame.draw.rect(screen, GRAY, (450, 250, 150, 120))
    screen.blit(font.render("Water Treatment Plant", True, BLACK), (450, 220))

    # ---------- TANK ----------
    pygame.draw.rect(screen, BLACK, (700, 220, 120, 220), 3)
    pygame.draw.rect(screen, BLUE, (700, 440 - tank_level, 120, tank_level))
    screen.blit(font.render("Clean Water Tank", True, BLACK), (700, 190))

    # ---------- FIELD ----------
    field_color = (30, int(field_health*2), 30)
    pygame.draw.rect(screen, field_color, (900, 250, 250, 150))
    screen.blit(font.render("Agricultural Field", True, BLACK), (950, 220))

    # ---------- FISH ----------
    for i in range(int(fish_population/15)):
        pygame.draw.circle(screen, DARK_BLUE, (random.randint(0, 900), random.randint(430, 500)), 4)

    # ---------- DASHBOARD ----------
    pygame.draw.rect(screen, BLACK, (50, 580, 600, 140), 2)

    for i in range(len(pollution_history)-1):
        pygame.draw.line(screen, RED,
                         (60 + i*2, 700 - pollution_history[i]),
                         (60 + (i+1)*2, 700 - pollution_history[i+1]), 2)

        pygame.draw.line(screen, GREEN,
                         (60 + i*2, 700 - fish_history[i]/2),
                         (60 + (i+1)*2, 700 - fish_history[i+1]/2), 2)

    screen.blit(font.render("Graph: Red=Pollution | Green=Fish Population", True, BLACK),
                (60, 550))

    # ---------- LEGEND ----------
    pygame.draw.rect(screen, BLACK, (700, 580, 550, 140), 2)

    legend_lines = [
        "Controls:",
        "A = Toggle AI Optimization",
        "UP/DOWN = Increase/Decrease Pollution Rate",
        "",
        "System Meaning:",
        "Red Line = River Pollution %",
        "Green Line = Fish Population",
        "Rain reduces pollution",
        "High pollution kills fish",
        "AI increases treatment when pollution rises",
    ]

    for i, line in enumerate(legend_lines):
        screen.blit(font.render(line, True, BLACK), (710, 590 + i*18))

    # ---------- STATS ----------
    stats = [
        f"River Pollution: {river_pollution:.1f}%",
        f"Sea Pollution: {sea_pollution:.1f}%",
        f"Fish Population: {fish_population:.1f}",
        f"Field Health: {field_health:.1f}",
        f"Treatment Efficiency: {treatment_efficiency:.2f}",
        f"Treatment Cost: ${treatment_cost:.0f}",
        f"Environmental Damage Cost: ${environmental_damage_cost:.0f}",
    ]

    for i, stat in enumerate(stats):
        screen.blit(font.render(stat, True, BLACK), (1050, 20 + i*20))

    if rain:
        screen.blit(font.render("Rain Event Active 🌧", True, BLUE), (50, 50))

    if ai_mode:
        screen.blit(font.render("AI Mode ON 🤖", True, RED), (50, 80))

    frame_count += 1
    pygame.display.flip()

pygame.quit()
sys.exit()
