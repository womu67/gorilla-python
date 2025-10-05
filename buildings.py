import pygame
import random
import math
from config import *


class Crater:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.lifetime = CRATER_DURATION
        self.max_lifetime = CRATER_DURATION
        self.color = random.choice(CRATER_COLORS)
        print(f"🔨 Neuer Krater bei ({x}, {y}) mit Radius {radius}")

    def update(self):
        self.lifetime -= 1
        return self.lifetime > 0

    def draw(self, screen):
        try:
            # Einfacher Krater ohne Transparenz für bessere Sichtbarkeit
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

            # Innere Schattierung
            inner_radius = max(3, self.radius // 2)
            inner_color = (
                max(0, self.color[0] - 30),
                max(0, self.color[1] - 30),
                max(0, self.color[2] - 30)
            )
            pygame.draw.circle(screen, inner_color, (int(self.x), int(self.y)), inner_radius)

        except Exception as e:
            print(f"❌ Fehler beim Zeichnen des Kraters: {e}")


def generate_buildings():
    buildings = []

    # Stelle sicher, dass Gebäude die gesamte Breite abdecken
    total_buildings = (WIDTH // BUILDING_WIDTH) + 2  # +2 für Überlappung

    for i in range(total_buildings):
        x = i * BUILDING_WIDTH

        # Wenn wir über den Rand gehen, anpassen
        if x >= WIDTH:
            break

        # Höhe variieren
        min_height = HEIGHT // 3
        max_height = HEIGHT * 2 // 3
        height = random.randint(min_height, max_height)

        # Letztes Gebäude anpassen
        building_width = BUILDING_WIDTH
        if x + building_width > WIDTH:
            building_width = WIDTH - x

        rect = pygame.Rect(x, HEIGHT - height, building_width, height)

        color_variation = random.randint(-80, 80)
        color = (
            max(min(BUILDING_COLOR[0] + color_variation, 255), 50),
            max(min(BUILDING_COLOR[1] + color_variation, 255), 50),
            max(min(BUILDING_COLOR[2] + color_variation, 255), 50)
        )

        windows = []
        window_w, window_h = 6, 8
        for y_pos in range(rect.top + 5, rect.bottom - window_h, window_h + 5):
            for xx in range(rect.left + 5, rect.right - window_w, window_w + 5):
                if random.random() > 0.7:
                    windows.append(pygame.Rect(xx, y_pos, window_w, window_h))

        buildings.append({
            "rect": rect,
            "color": color,
            "windows": windows,
            "craters": []
        })

    print(f"🏢 {len(buildings)} Gebäude generiert für {WIDTH}x{HEIGHT}")
    return buildings


def add_crater_to_building(buildings, impact_x, impact_y):
    """Fügt einen Krater an der Einschlagstelle hinzu"""
    if impact_x is None or impact_y is None:
        print("❌ Keine gültige Einschlagposition")
        return False

    print(f"🎯 Suche Gebäude für Einschlag bei ({impact_x:.1f}, {impact_y:.1f})")

    for i, building in enumerate(buildings):
        building_rect = building["rect"]

        # Erweiterte Kollisionsprüfung mit Toleranz
        tolerance = 10  # Pixel Toleranz
        expanded_rect = building_rect.inflate(tolerance, tolerance)

        if expanded_rect.collidepoint(impact_x, impact_y):
            # Krater-Größe
            crater_radius = random.randint(12, CRATER_MAX_RADIUS)

            # Stelle sicher, dass der Krater innerhalb des Gebäudes bleibt
            crater_x = max(building_rect.left + crater_radius,
                           min(impact_x, building_rect.right - crater_radius))
            crater_y = max(building_rect.top + crater_radius,
                           min(impact_y, building_rect.bottom - crater_radius))

            crater = Crater(crater_x, crater_y, crater_radius)
            building["craters"].append(crater)

            print(f"💥 Krater zu Gebäude {i} hinzugefügt")
            print(f"   Position: ({crater_x:.1f}, {crater_y:.1f})")
            print(f"   Gebäude-Bereich: {building_rect}")
            return True

    print(f"❌ Kein Gebäude an Position ({impact_x:.1f}, {impact_y:.1f}) gefunden")
    return False


def update_building_craters(buildings):
    """Krater werden nicht mehr upgedatet - sie sind permanent"""
    # Keine Aktion mehr - Krater bleiben permanent
    pass


def draw_buildings(screen, buildings):
    total_craters = 0

    for b in buildings:
        # Gebäude ohne Krater zeichnen
        pygame.draw.rect(screen, b["color"], b["rect"])

        # Fenster zeichnen (vor den Kratern)
        for w in b["windows"]:
            pygame.draw.rect(screen, (255, 255, 100), w)

        # Krater als "Löcher" zeichnen - wir zeichnen sie nicht, sie sind Löcher
        total_craters += len(b["craters"])

    # Jetzt zeichnen wir die Krater-Ränder für bessere Sichtbarkeit
    for b in buildings:
        for crater in b["craters"]:
            _draw_crater_outline(screen, crater)

    # Debug-Info anzeigen
    if total_craters > 0:
        debug_text = f"Krater: {total_craters}"
        font = pygame.font.SysFont(None, 24)
        text_surface = font.render(debug_text, True, (255, 255, 255))
        screen.blit(text_surface, (10, HEIGHT - 30))


def _draw_crater_outline(screen, crater):
    """Zeichnet nur den Rand des Kraters für bessere Sichtbarkeit"""
    try:
        # Krater-Rand (dunkler Ring)
        pygame.draw.circle(screen, (40, 40, 40), (int(crater.x), int(crater.y)), crater.radius, 3)

        # Innerer Schatten für Tiefenwirkung
        inner_radius = max(2, crater.radius - 4)
        pygame.draw.circle(screen, (30, 30, 30), (int(crater.x), int(crater.y)), inner_radius, 2)

    except Exception as e:
        print(f"❌ Fehler beim Zeichnen des Krater-Rands: {e}")