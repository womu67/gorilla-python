import pygame
import sys
import math
import random

# Einfache Konfiguration für Web
WIDTH, HEIGHT = 800, 600
BUILDING_WIDTH = 50
GORILLA_SIZE = 30
GRAVITY = 0.5


class Gorilla:
    def __init__(self, x, y, color, player_number):
        self.x = x
        self.y = y
        self.color = color
        self.player_number = player_number
        self.angle = 45
        self.velocity = 25

    def draw(self, screen):
        # Einfache Darstellung für Web
        pygame.draw.circle(screen, self.color, (self.x, self.y - GORILLA_SIZE), GORILLA_SIZE)

    def get_throw_position(self):
        if self.player_number == 1:
            return self.x + 20, self.y - GORILLA_SIZE
        else:
            return self.x - 20, self.y - GORILLA_SIZE


class Banana:
    def __init__(self, x, y, angle, velocity, direction):
        self.x = x
        self.y = y
        self.vel_x = velocity * math.cos(math.radians(angle)) * direction
        self.vel_y = -velocity * math.sin(math.radians(angle))
        self.active = True

    def update(self, wind):
        self.vel_x += wind * 0.05
        self.vel_y += GRAVITY
        self.x += self.vel_x
        self.y += self.vel_y

        if self.x < 0 or self.x > WIDTH or self.y > HEIGHT:
            self.active = False

        return self.active

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 0), (int(self.x), int(self.y)), 5)


def generate_buildings():
    buildings = []
    for i in range(WIDTH // BUILDING_WIDTH):
        x = i * BUILDING_WIDTH
        height = random.randint(100, 300)
        rect = pygame.Rect(x, HEIGHT - height, BUILDING_WIDTH, height)
        buildings.append(rect)
    return buildings


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    buildings = generate_buildings()
    gorilla1 = Gorilla(buildings[0].centerx, buildings[0].top, (255, 0, 0), 1)
    gorilla2 = Gorilla(buildings[-1].centerx, buildings[-1].top, (0, 0, 255), 2)

    banana = None
    current_player = 1
    wind = random.uniform(-2, 2)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and current_player == 1:
                    banana = Banana(*gorilla1.get_throw_position(), gorilla1.angle, gorilla1.velocity, 1)
                    current_player = 2
                elif event.key == pygame.K_RETURN and current_player == 2:
                    banana = Banana(*gorilla2.get_throw_position(), gorilla2.angle, gorilla2.velocity, -1)
                    current_player = 1

        screen.fill((135, 206, 235))

        # Gebäude zeichnen
        for building in buildings:
            pygame.draw.rect(screen, (100, 100, 100), building)

        # Gorillas zeichnen
        gorilla1.draw(screen)
        gorilla2.draw(screen)

        # Banane aktualisieren und zeichnen
        if banana and banana.active:
            banana.active = banana.update(wind)
            banana.draw(screen)
        elif banana and not banana.active:
            banana = None
            wind = random.uniform(-2, 2)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()