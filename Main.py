# -*- coding: utf-8 -*-
import pygame
import sys
from game_logic import Game
from ui import draw_scene
from config import FPS, WIDTH, HEIGHT


def main():
    print("Starte Gorillas Spiel...")

    try:
        # Pygame initialisieren
        pygame.init()
        print("Pygame initialisiert")

        # Display mit fester Auflösung setzen
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Gorillas Python")
        print(f"Display erstellt: {WIDTH}x{HEIGHT}")

        # Spiel erstellen
        game = Game()
        print("Spielinstanz erstellt")

        print("\n" + "=" * 60)
        print("GORILLAS SPIEL GESTARTET!")
        print("=" * 60)
        print("PLAYER 1 (LINKS, ROT):")
        print("   W/S - Winkel aendern (0-90°)")
        print("   A/D - Geschwindigkeit aendern (10-80)")
        print("   LEERTASTE - Werfen")
        print("")
        print("PLAYER 2 (RECHTS, BLAU):")
        print("   PFEIL HOCH/RUNTER - Winkel aendern (0-90°)")
        print("   PFEIL LINKS/RECHTS - Geschwindigkeit aendern (10-80)")
        print("   ENTER - Werfen")
        print("=" * 60)
        print("Das Spiel laeuft jetzt... Viel Spass!")

        # Hauptspielschleife
        running = True
        frame_count = 0

        while running:
            frame_count += 1

            # Events verarbeiten
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    print("Spiel beendet")
                else:
                    game.handle_input(event)

            # Spiel logik aktualisieren
            game.update()

            # Szene zeichnen
            draw_scene(screen, game)

            # FPS kontrollieren
            game.clock.tick(FPS)

            # Debug: Zeige alle 500 Frames dass das Spiel laeuft
            if frame_count % 500 == 0:
                print(f"Spiel laeuft... Frame {frame_count}, Aktiver Spieler: {game.current_player}")

    except Exception as e:
        print(f"KRITISCHER FEHLER: {e}")
        import traceback
        traceback.print_exc()

    finally:
        print("Raeume auf...")
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    main()
    print("Programm beendet")