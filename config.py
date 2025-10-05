import pygame

# Einfache feste Werte
WIDTH, HEIGHT = 1200, 800
BUILDING_WIDTH = 60
GORILLA_SIZE = 40
GRAVITY = 0.5
FPS = 60

# Colors
SKY = (135, 206, 235)
BUILDING_COLOR = (100, 100, 100)
GORILLA_COLOR = (255, 0, 0)
GORILLA2_COLOR = (0, 0, 255)
BANANA_COLOR = (255, 255, 0)

# Krater-Farben (dunklere Grautöne für bessere Sichtbarkeit)
CRATER_COLORS = [
    (60, 60, 60),    # Sehr dunkelgrau
    (70, 70, 70),    # Dunkelgrau
    (50, 50, 50),    # Fast schwarz
]

# Krater-Einstellungen - PERMANENT
CRATER_DURATION = 0  # 0 = unendlich, Krater bleiben bis zum Rundenende
CRATER_MAX_RADIUS = 25  # Etwas größere Krater

# Player Controls
PLAYER1_CONTROLS = {
    'angle_up': pygame.K_w,
    'angle_down': pygame.K_s,
    'velocity_up': pygame.K_d,
    'velocity_down': pygame.K_a,
    'throw': pygame.K_SPACE
}

PLAYER2_CONTROLS = {
    'angle_up': pygame.K_UP,
    'angle_down': pygame.K_DOWN,
    'velocity_up': pygame.K_RIGHT,
    'velocity_down': pygame.K_LEFT,
    'throw': pygame.K_RETURN
}

SCALE_X = 1.0
SCALE_Y = 1.0