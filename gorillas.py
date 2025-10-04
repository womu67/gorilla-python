import pygame
import math
from config import *


class Gorilla:
    def __init__(self, x, y, color, player_number):
        self.x = x
        self.y = y
        self.color = color
        self.player_number = player_number
        self.angle = 45
        self.velocity = 25
        self.throw_animation = 0

    def _lighten_color(self, color, amount=30):
        return tuple(min(255, c + amount) for c in color)

    def _draw_body(self, screen):
        # Körper - größer und zentriert
        body_width = GORILLA_SIZE + 10
        body_height = GORILLA_SIZE + 10
        body_rect = pygame.Rect(
            self.x - body_width // 2,
            self.y - body_height // 2,
            body_width,
            body_height
        )
        pygame.draw.ellipse(screen, self.color, body_rect)

        # Bauch - etwas hellere Farbe

        belly_color = self._lighten_color(self.color, 30)
        face_color = self._lighten_color(self.color, 20)
        belly_width = body_width * 0.8
        belly_height = body_height * 0.8
        belly_rect = pygame.Rect(
            self.x - belly_width // 2,
            self.y - belly_height // 2,
            belly_width,
            belly_height
        )
        pygame.draw.ellipse(screen, belly_color, belly_rect)

    def _draw_face(self, screen):
        # Kopf über dem Körper
        head_radius = GORILLA_SIZE // 2 + 5
        head_y = self.y - GORILLA_SIZE - 5

        pygame.draw.circle(screen, self.color, (self.x, head_y), head_radius)

        # Gesicht - etwas heller
        face_color = (
            min(255, self.color[0] + 20),
            min(255, self.color[1] + 20),
            min(255, self.color[2] + 20)
        )
        face_radius = head_radius - 3
        pygame.draw.circle(screen, face_color, (self.x, head_y), face_radius)

        # Augen
        eye_offset = 10 if self.player_number == 1 else -10
        eye_y = head_y - 5

        # Weiß der Augen
        pygame.draw.circle(screen, (255, 255, 255), (self.x - eye_offset, eye_y), 8)
        pygame.draw.circle(screen, (255, 255, 255), (self.x + eye_offset, eye_y), 8)

        # Pupillen
        pupil_offset = 3 if self.player_number == 1 else -3
        pygame.draw.circle(screen, (0, 0, 0), (self.x - eye_offset + pupil_offset, eye_y), 4)
        pygame.draw.circle(screen, (0, 0, 0), (self.x + eye_offset + pupil_offset, eye_y), 4)

        # Mund
        mouth_y = head_y + 10
        if self.throw_animation > 0:
            # Offener Mund beim Werfen
            pygame.draw.ellipse(screen, (0, 0, 0),
                                (self.x - 8, mouth_y - 3, 16, 10))
        else:
            # Geschlossener Mund
            pygame.draw.arc(screen, (0, 0, 0),
                            (self.x - 10, mouth_y - 3, 20, 8), 0, 3.14, 3)

    def _draw_normal_arms(self, screen):
        # Schulter-Positionen (seitlich am Körper)
        shoulder_height = self.y - GORILLA_SIZE // 4
        arm_length = GORILLA_SIZE + 5  # VON 15 AUF 5 REDUZIERT
        arm_thickness = 10  # AUCH ETWAS DÜNNER

        if self.player_number == 1:
            # Spieler 1 (links)
            left_shoulder_x = self.x - GORILLA_SIZE // 2 - 5
            right_shoulder_x = self.x + GORILLA_SIZE // 2 + 5

            # Linker Arm (hängt runter)
            left_arm_points = [
                (left_shoulder_x, shoulder_height),
                (left_shoulder_x - arm_length // 3, shoulder_height + arm_length // 2),
                (left_shoulder_x - arm_length // 2, shoulder_height + arm_length)
            ]

            # Rechter Arm (etwas angewinkelt)
            right_arm_points = [
                (right_shoulder_x, shoulder_height),
                (right_shoulder_x + arm_length // 4, shoulder_height - arm_length // 3),
                (right_shoulder_x + arm_length // 2, shoulder_height - arm_length // 2)
            ]
        else:
            # Spieler 2 (rechts) - gespiegelt
            left_shoulder_x = self.x - GORILLA_SIZE // 2 - 5
            right_shoulder_x = self.x + GORILLA_SIZE // 2 + 5

            # Linker Arm (etwas angewinkelt - Wurfarm)
            left_arm_points = [
                (left_shoulder_x, shoulder_height),
                (left_shoulder_x - arm_length // 4, shoulder_height - arm_length // 3),
                (left_shoulder_x - arm_length // 2, shoulder_height - arm_length // 2)
            ]

            # Rechter Arm (hängt runter)
            right_arm_points = [
                (right_shoulder_x, shoulder_height),
                (right_shoulder_x + arm_length // 3, shoulder_height + arm_length // 2),
                (right_shoulder_x + arm_length // 2, shoulder_height + arm_length)
            ]

        # Arme zeichnen
        pygame.draw.lines(screen, self.color, False, left_arm_points, arm_thickness)
        pygame.draw.lines(screen, self.color, False, right_arm_points, arm_thickness)

        # Hände zeichnen
        pygame.draw.circle(screen, self.color, left_arm_points[-1], 10)
        pygame.draw.circle(screen, self.color, right_arm_points[-1], 10)

    def _draw_throwing_arms(self, screen):
        # Animation-Fortschritt (0 bis 1)
        progress = 1 - (self.throw_animation / 60.0)

        # Arm-Länge während der Animation variieren - KÜRZER
        base_arm_length = GORILLA_SIZE + 10  # VON 20 AUF 10 REDUZIERT
        animated_arm_length = base_arm_length * (0.8 + 0.4 * progress)

        # Schulter-Positionen
        shoulder_height = self.y - GORILLA_SIZE // 4
        arm_length = GORILLA_SIZE + 10  # AUCH HIER ANPASSEN
        arm_thickness = 10  # ETWAS DÜNNERILLA_SIZE + 20

        if self.player_number == 1:
            # Spieler 1 wirft mit rechtem Arm
            left_shoulder_x = self.x - GORILLA_SIZE // 2 - 5
            right_shoulder_x = self.x + GORILLA_SIZE // 2 + 5

            # Linker Arm (hängt runter)
            left_arm_points = [
                (left_shoulder_x, shoulder_height),
                (left_shoulder_x - arm_length // 3, shoulder_height + arm_length // 2),
                (left_shoulder_x - arm_length // 2, shoulder_height + arm_length)
            ]

            # Rechter Wurfarm (gestreckt)
            angle_rad = math.radians(self.angle)
            throw_hand_x = right_shoulder_x + arm_length * math.cos(angle_rad)
            throw_hand_y = shoulder_height - arm_length * math.sin(angle_rad)

            right_arm_points = [
                (right_shoulder_x, shoulder_height),
                (right_shoulder_x + arm_length * 0.3 * math.cos(angle_rad),
                 shoulder_height - arm_length * 0.3 * math.sin(angle_rad)),
                (throw_hand_x, throw_hand_y)
            ]
        else:
            # Spieler 2 wirft mit linkem Arm
            left_shoulder_x = self.x - GORILLA_SIZE // 2 - 5
            right_shoulder_x = self.x + GORILLA_SIZE // 2 + 5

            # Linker Wurfarm (gestreckt)
            angle_rad = math.radians(180 - self.angle)
            throw_hand_x = left_shoulder_x + arm_length * math.cos(angle_rad)
            throw_hand_y = shoulder_height - arm_length * math.sin(angle_rad)

            left_arm_points = [
                (left_shoulder_x, shoulder_height),
                (left_shoulder_x + arm_length * 0.3 * math.cos(angle_rad),
                 shoulder_height - arm_length * 0.3 * math.sin(angle_rad)),
                (throw_hand_x, throw_hand_y)
            ]

            # Rechter Arm (hängt runter)
            right_arm_points = [
                (right_shoulder_x, shoulder_height),
                (right_shoulder_x + arm_length // 3, shoulder_height + arm_length // 2),
                (right_shoulder_x + arm_length // 2, shoulder_height + arm_length)
            ]

        # Rest des Codes anpassen...
        if self.player_number == 1:
            throw_hand_x = right_shoulder_x + animated_arm_length * math.cos(angle_rad)
            throw_hand_y = shoulder_height - animated_arm_length * math.sin(angle_rad)
        else:
            throw_hand_x = left_shoulder_x + animated_arm_length * math.cos(angle_rad)
            throw_hand_y = shoulder_height - animated_arm_length * math.sin(angle_rad)

        # Arme zeichnen
        pygame.draw.lines(screen, self.color, False, left_arm_points, arm_thickness)
        pygame.draw.lines(screen, self.color, False, right_arm_points, arm_thickness)

        # Hände zeichnen
        pygame.draw.circle(screen, self.color, left_arm_points[-1], 10)
        pygame.draw.circle(screen, self.color, right_arm_points[-1], 10)

    def start_throw_animation(self):
        print(f"🦍 Throw animation started for Player {self.player_number}")  # DEBUG
        self.throw_animation = 45  # Etwas kürzer für besseren Flow

    def draw(self, screen):
        self._draw_body(screen)
        self._draw_face(screen)

        # Arme zeichnen - Animation langsamer reduzieren
        if self.throw_animation > 0:
            self._draw_throwing_arms(screen)
            self.throw_animation -= 0.7  # Langsamer reduzieren
            # Debug-Ausgabe für Animation
            if self.throw_animation % 10 == 0:  # Nur alle 10 Frames loggen
                print(f"🔄 Animation frame: {self.throw_animation}")
        else:
            self._draw_normal_arms(screen)

    def get_throw_position(self):
        # Schulter-Position
        shoulder_height = self.y - GORILLA_SIZE // 4
        arm_length = GORILLA_SIZE + 10  # AUCH HIER KÜRZER

        if self.player_number == 1:
            # Spieler 1 wirft mit rechtem Arm
            shoulder_x = self.x + GORILLA_SIZE // 2 + 5
            angle_rad = math.radians(self.angle)
            x = shoulder_x + arm_length * math.cos(angle_rad)
            y = shoulder_height - arm_length * math.sin(angle_rad)
        else:
            # Spieler 2 wirft mit linkem Arm
            shoulder_x = self.x - GORILLA_SIZE // 2 - 5
            angle_rad = math.radians(180 - self.angle)
            x = shoulder_x + arm_length * math.cos(angle_rad)
            y = shoulder_height - arm_length * math.sin(angle_rad)

        return x, y

    def update_angle(self, change):
        new_angle = self.angle + change
        self.angle = max(1, min(89, new_angle))  # 0° und 90° vermeiden

    def update_velocity(self, change):
        new_velocity = self.velocity + change
        self.velocity = max(5, min(100, new_velocity))  # realistischer Bereich