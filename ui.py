import pygame
from config import *
from buildings import draw_buildings


def draw_ui(screen, font, game):
    # Größere Schrift für größeres Spielfeld
    large_font = pygame.font.SysFont(None, 28)

    # Score und Wind - oben links und rechts
    score_bg = pygame.Rect(5, 5, 250, 35)
    pygame.draw.rect(screen, (0, 0, 0, 128), score_bg, border_radius=5)
    score_text = large_font.render(f"Score: P1 {game.score1} - P2 {game.score2}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    wind_bg = pygame.Rect(WIDTH - 130, 5, 125, 35)
    pygame.draw.rect(screen, (0, 0, 0, 128), wind_bg, border_radius=5)
    wind_text = large_font.render(f"Wind: {game.wind:+.1f}", True, (255, 255, 255))
    screen.blit(wind_text, (WIDTH - 125, 10))

    # Info-Bereich unten mit farbigem Hintergrund
    info_height = 90  # Höherer Info-Bereich
    info_rect = pygame.Rect(0, HEIGHT - info_height, WIDTH, info_height)

    # Hintergrundfarbe basierend auf aktuellem Spieler
    if game.current_player == 1:
        bg_color = (255, 0, 0, 128)  # Rot für Spieler 1
    else:
        bg_color = (0, 0, 255, 128)  # Blau für Spieler 2

    pygame.draw.rect(screen, bg_color, info_rect)

    # Rahmen um den Info-Bereich
    pygame.draw.rect(screen, (255, 255, 255), info_rect, 2)

    # Spieler-Info und Steuerung
    y_position = HEIGHT - 75

    if game.current_player == 1:
        player_text = large_font.render(
            f"Player 1 am Zug | Winkel: {game.gorilla1.angle}° | Geschwindigkeit: {game.gorilla1.velocity}", True,
            (255, 255, 255))
        controls_text1 = large_font.render("Steuerung: W/S = Winkel | A/D = Geschwindigkeit | LEERTASTE = Werfen", True,
                                           (255, 255, 255))

        screen.blit(player_text, (WIDTH // 2 - player_text.get_width() // 2, y_position))
        screen.blit(controls_text1, (WIDTH // 2 - controls_text1.get_width() // 2, y_position + 30))
    else:
        player_text = large_font.render(
            f"Player 2 am Zug | Winkel: {game.gorilla2.angle}° | Geschwindigkeit: {game.gorilla2.velocity}", True,
            (255, 255, 255))
        controls_text1 = large_font.render(
            "Steuerung: PFEIL HOCH/RUNTER = Winkel | PFEIL LINKS/RECHTS = Geschwindigkeit", True, (255, 255, 255))
        controls_text2 = large_font.render("ENTER = Werfen", True, (255, 255, 255))

        screen.blit(player_text, (WIDTH // 2 - player_text.get_width() // 2, y_position))
        screen.blit(controls_text1, (WIDTH // 2 - controls_text1.get_width() // 2, y_position + 30))
        screen.blit(controls_text2, (WIDTH // 2 - controls_text2.get_width() // 2, y_position + 60))


def draw_scene(screen, game):
    screen.fill(SKY)

    # Gebäude zeichnen
    draw_buildings(screen, game.buildings)

    # Gorillas zeichnen
    game.gorilla1.draw(screen)
    game.gorilla2.draw(screen)

    # UI zeichnen
    draw_ui(screen, game.font, game)

    # Banane zeichnen
    if game.banana and game.banana.active:
        game.banana.draw(screen)

    pygame.display.flip()