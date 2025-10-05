import pygame
import math
from config import *
from buildings import add_crater_to_building


class Banana:
    def __init__(self, x, y, angle, velocity, direction, thrower):
        self.x = x
        self.y = y
        self.thrower = thrower
        self.trail = []
        self.max_trail_length = 12
        rad = math.radians(angle)

        if direction == 1:
            self.vel_x = velocity * math.cos(rad)
        else:
            self.vel_x = -velocity * math.cos(rad)

        self.vel_y = -velocity * math.sin(rad)
        self.active = True
        self.frames_active = 0
        self.last_x = x
        self.last_y = y
        self.impact_x = None
        self.impact_y = None

    def update(self, wind, buildings, gorilla1, gorilla2):
        if not self.active:
            return False, None

        self.frames_active += 1

        # Vorherige Position speichern
        self.last_x = self.x
        self.last_y = self.y

        # Physik anwenden
        self.vel_x += wind * 0.05
        self.vel_y += GRAVITY
        self.x += self.vel_x
        self.y += self.vel_y

        # Trail aktualisieren
        self.trail.append((self.x, self.y))
        if len(self.trail) > self.max_trail_length:
            self.trail.pop(0)

        # Einfache Kollisionsprüfung - nur aktueller Punkt
        collision = self.check_simple_collision(buildings, gorilla1, gorilla2)
        if collision:
            self.active = False
            self.impact_x = self.x
            self.impact_y = self.y
            print(f"💥 Kollision bei ({self.impact_x:.1f}, {self.impact_y:.1f})")
            return True, collision

        # Grenzen prüfen
        if self.x < 0 or self.x > WIDTH or self.y > HEIGHT:
            self.active = False
            return True, "out_of_bounds"

        return False, None

    def check_simple_collision(self, buildings, gorilla1, gorilla2):
        """Kollisionsprüfung die Krater als Löcher berücksichtigt"""
        # Warte ein paar Frames, um Selbstkollision zu vermeiden
        if self.frames_active < 8:
            return None

        # Prüfe Gorilla-Kollision zuerst
        gorilla_collision = self.check_gorilla_collision(gorilla1, gorilla2)
        if gorilla_collision:
            return gorilla_collision

        # Prüfe Gebäude-Kollision - ABER IGNORIERE BEREICHE MIT KRATERN
        point_rect = pygame.Rect(self.x - 5, self.y - 5, 10, 10)

        for building in buildings:
            building_rect = building["rect"]

            # Prüfe zuerst ob Punkt im Gebäude ist
            if building_rect.colliderect(point_rect):
                # Prüfe ob Punkt in einem Krater liegt (dann KEINE Kollision)
                in_crater = False
                for crater in building["craters"]:
                    distance = math.sqrt((self.x - crater.x) ** 2 + (self.y - crater.y) ** 2)
                    if distance <= crater.radius:
                        in_crater = True
                        break

                # Nur Kollision wenn nicht in einem Krater
                if not in_crater:
                    return "building"

        return None
    def _check_line_building_collision(self, x1, y1, x2, y2, building_rect):
        """Prüft Kollision zwischen Liniensegment und Gebäuderechteck"""
        # Vereinfachte Prüfung: Teile die Linie in mehrere Punkte auf
        steps = 10  # Anzahl der Zwischenpunkte
        for i in range(steps + 1):
            t = i / steps
            check_x = x1 + (x2 - x1) * t
            check_y = y1 + (y2 - y1) * t

            # Prüfe ob dieser Punkt im Gebäude ist
            point_rect = pygame.Rect(check_x - 4, check_y - 4, 8, 8)
            if building_rect.colliderect(point_rect):
                # Aktualisiere die Position für genaue Kollisionserkennung
                self.x = check_x
                self.y = check_y
                return True

        return False

    def check_gorilla_collision(self, gorilla1, gorilla2):
        point_rect = pygame.Rect(self.x - 8, self.y - 8, 16, 16)

        gor1_rect = pygame.Rect(gorilla1.x - 25, gorilla1.y - 40, 50, 50)
        gor2_rect = pygame.Rect(gorilla2.x - 25, gorilla2.y - 40, 50, 50)

        if self.thrower == 1:
            if gor2_rect.colliderect(point_rect):
                return "player2"
        else:
            if gor1_rect.colliderect(point_rect):
                return "player1"

        return None

    def get_impact_position(self):
        return self.impact_x, self.impact_y

    def draw(self, screen):
        # Trail zeichnen
        for i, pos in enumerate(self.trail):
            alpha = i / len(self.trail) if self.trail else 0
            trail_size = max(2, int(4 * alpha))
            trail_color = (255, 255, int(200 * (1 - alpha)))
            pygame.draw.circle(screen, trail_color, (int(pos[0]), int(pos[1])), trail_size)

        # Banane zeichnen
        pygame.draw.circle(screen, BANANA_COLOR, (int(self.x), int(self.y)), 7)