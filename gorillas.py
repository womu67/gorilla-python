import pygame
from config import *


class Gorilla:
    def __init__(self, x, y, color, player_number):
        self.x = x
        self.y = y
        self.color = color
        self.player_number = player_number
        self.angle = 45
        self.velocity = 25  # Feste Geschwindigkeit

    def draw(self, screen):
        # Körper
        pygame.draw.circle(screen, self.color, (self.x, self.y), GORILLA_SIZE // 2)
        # Kopf
        pygame.draw.circle(screen, self.color, (self.x, self.y - GORILLA_SIZE // 2), GORILLA_SIZE // 3)

        # Arme (position basierend auf Spieler)
        arm_offset = 8 if self.player_number == 1 else -8
        pygame.draw.circle(screen, self.color, (self.x + arm_offset, self.y - 8), GORILLA_SIZE // 5)

        # Beine
        pygame.draw.circle(screen, self.color, (self.x - GORILLA_SIZE // 4, self.y + GORILLA_SIZE // 2),
                           GORILLA_SIZE // 5)
        pygame.draw.circle(screen, self.color, (self.x + GORILLA_SIZE // 4, self.y + GORILLA_SIZE // 2),
                           GORILLA_SIZE // 5)

        # Augen
        eye_offset = 5 if self.player_number == 1 else -5
        pygame.draw.circle(screen, (255, 255, 255), (self.x - eye_offset, self.y - GORILLA_SIZE // 2), 5)
        pygame.draw.circle(screen, (255, 255, 255), (self.x + eye_offset, self.y - GORILLA_SIZE // 2), 5)
        pygame.draw.circle(screen, (0, 0, 0), (self.x - eye_offset, self.y - GORILLA_SIZE // 2), 3)
        pygame.draw.circle(screen, (0, 0, 0), (self.x + eye_offset, self.y - GORILLA_SIZE // 2), 3)

    def get_throw_position(self):
        return self.x, self.y - GORILLA_SIZE - 10

    def update_angle(self, change):
        self.angle = max(0, min(90, self.angle + change))

    def update_velocity(self, change):
        self.velocity = max(10, min(80, self.velocity + change))