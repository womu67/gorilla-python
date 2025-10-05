import pygame
import random
import math
from config import *
from buildings import generate_buildings, add_crater_to_building, update_building_craters
from gorillas import Gorilla
from banana import Banana


class Game:
    def __init__(self):
        print("🛠️  Erstelle Spielinstanz...")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 24)

        self.round_count = 0
        self.reset_game()
        self.setup_sounds()

        print("✅ Spiel erfolgreich initialisiert!")
        print(f"   Spielfeld: {WIDTH}x{HEIGHT}")
        print(f"   Gebäudekollision: AKTIV")
        print(f"   Kratereffekte: AKTIV")

    def reset_game(self):
        print("🏗️  Generiere Gebäude...")
        self.buildings = generate_buildings()

        first_building = self.buildings[0]
        self.gorilla1 = Gorilla(
            first_building["rect"].centerx,
            first_building["rect"].top - GORILLA_SIZE,
            GORILLA_COLOR, 1
        )

        last_building = self.buildings[-1]
        self.gorilla2 = Gorilla(
            last_building["rect"].centerx,
            last_building["rect"].top - GORILLA_SIZE,
            GORILLA2_COLOR, 2
        )

        self.score1 = 0
        self.score2 = 0
        self.banana = None
        self.waiting_for_input = True
        self.wind = random.uniform(-3.0, 3.0)

        self.round_count += 1
        if self.round_count % 2 == 1:
            self.current_player = 1
            print(f"🎯 Runde {self.round_count}: Player 1 (ROT) beginnt!")
        else:
            self.current_player = 2
            print(f"🎯 Runde {self.round_count}: Player 2 (BLAU) beginnt!")

    def update(self):
        # KRATER-UPDATE ENTFERNEN - sie sind jetzt permanent
        # update_building_craters(self.buildings)  # DIESE ZEILE AUSKOMMENTIEREN ODER LÖSCHEN

        if self.banana and self.banana.active:
            collision_occurred, collision_type = self.banana.update(
                self.wind, self.buildings, self.gorilla1, self.gorilla2
            )

            if collision_occurred:
                print(f"💥 Kollision: {collision_type}")

                if collision_type in ["player1", "player2"]:
                    self.hit_sound.play()
                    self.handle_game_over(collision_type)
                elif collision_type == "building":
                    self.building_hit_sound.play()
                    print("🏢 Gebäude getroffen! Erzeuge Krater...")

                    # Krater an der Einschlagstelle hinzufügen
                    impact_x, impact_y = self.banana.get_impact_position()
                    if impact_x and impact_y:
                        add_crater_to_building(self.buildings, impact_x, impact_y)

                    self.switch_player()
                else:
                    self.switch_player()

        elif self.banana and not self.banana.active:
            self.switch_player()

    def setup_sounds(self):
        try:
            # Lautstärke-Einstellungen (0.0 = leise, 1.0 = laut)
            VOLUME_HIT = 0.3  # 30% Lautstärke für Treffer
            VOLUME_BUILDING = 0.2  # 20% Lautstärke für Gebäude
            VOLUME_THROW = 0.1  # 10% Lautstärke für Wurf

            # Treffer-Sound (für Gorilla)
            sample_rate = 44100
            duration = 0.15  # Kürzere Dauer
            frames = int(duration * sample_rate)
            buffer = bytearray()
            for i in range(frames):
                # Sanftere Frequenz für Treffer-Sound
                value = int(80 + 80 * math.sin(2 * math.pi * 550 * i / sample_rate))  # Reduzierte Amplitude
                buffer.append(value)
            self.hit_sound = pygame.mixer.Sound(buffer=bytes(buffer))
            self.hit_sound.set_volume(VOLUME_HIT)

            # Gebäude-Kollisionssound (sehr leise)
            building_buffer = bytearray()
            for i in range(frames):
                # Sehr leiser tiefer Sound
                value = int(60 + 60 * math.sin(2 * math.pi * 180 * i / sample_rate))  # Stärker reduziert
                building_buffer.append(value)
            self.building_hit_sound = pygame.mixer.Sound(buffer=bytes(building_buffer))
            self.building_hit_sound.set_volume(VOLUME_BUILDING)

            # Wurf-Sound (sehr leise und kurz)
            throw_duration = 0.08  # Sehr kurz
            throw_frames = int(throw_duration * sample_rate)
            throw_buffer = bytearray()
            for i in range(throw_frames):
                value = int(50 + 50 * math.sin(2 * math.pi * 300 * i / sample_rate))  # Sehr leise
                throw_buffer.append(value)
            self.throw_sound = pygame.mixer.Sound(buffer=bytes(throw_buffer))
            self.throw_sound.set_volume(VOLUME_THROW)

            print("🔊 Leise Sounds erfolgreich geladen")
            print(
                f"   📢 Lautstärken: Treffer {VOLUME_HIT * 100}%, Gebäude {VOLUME_BUILDING * 100}%, Wurf {VOLUME_THROW * 100}%")

        except Exception as e:
            print(f"❌ Fehler beim Laden der Sounds: {e}")
            # Fallback-Sounds mit reduzierter Lautstärke
            self.hit_sound = pygame.mixer.Sound(buffer=bytes([100] * 800))  # Leiser
            self.building_hit_sound = pygame.mixer.Sound(buffer=bytes([80] * 600))  # Noch leiser
            self.throw_sound = pygame.mixer.Sound(buffer=bytes([60] * 400))  # Am leisesten

            # Lautstärke für Fallback-Sounds setzen
            self.hit_sound.set_volume(0.2)
            self.building_hit_sound.set_volume(0.15)
            self.throw_sound.set_volume(0.1)

    def handle_input(self, event):
        if not self.waiting_for_input:
            return

        if event.type == pygame.KEYDOWN:
            # Player 1 Steuerung
            if self.current_player == 1:
                if event.key == PLAYER1_CONTROLS['angle_up']:
                    self.gorilla1.update_angle(5)
                elif event.key == PLAYER1_CONTROLS['angle_down']:
                    self.gorilla1.update_angle(-5)
                elif event.key == PLAYER1_CONTROLS['velocity_up']:
                    self.gorilla1.update_velocity(1)
                elif event.key == PLAYER1_CONTROLS['velocity_down']:
                    self.gorilla1.update_velocity(-1)
                elif event.key == PLAYER1_CONTROLS['throw']:
                    print(f"🎯 Player 1 wirft! Winkel: {self.gorilla1.angle}°, Geschw: {self.gorilla1.velocity}")
                    self.throw_banana()

            # Player 2 Steuerung
            elif self.current_player == 2:
                if event.key == PLAYER2_CONTROLS['angle_up']:
                    self.gorilla2.update_angle(5)
                elif event.key == PLAYER2_CONTROLS['angle_down']:
                    self.gorilla2.update_angle(-5)
                elif event.key == PLAYER2_CONTROLS['velocity_up']:
                    self.gorilla2.update_velocity(1)
                elif event.key == PLAYER2_CONTROLS['velocity_down']:
                    self.gorilla2.update_velocity(-1)
                elif event.key == PLAYER2_CONTROLS['throw']:
                    print(f"🎯 Player 2 wirft! Winkel: {self.gorilla2.angle}°, Geschw: {self.gorilla2.velocity}")
                    self.throw_banana()

    def throw_banana(self):
        if self.current_player == 1:
            # ANIMATION STARTEN FÜR PLAYER 1
            self.gorilla1.start_throw_animation()
            x, y = self.gorilla1.get_throw_position()
            self.banana = Banana(x, y, self.gorilla1.angle, self.gorilla1.velocity, 1, 1)
            print(f"🎯 Player 1 wirft von Position ({x:.1f}, {y:.1f})")
        else:
            # ANIMATION STARTEN FÜR PLAYER 2
            self.gorilla2.start_throw_animation()
            x, y = self.gorilla2.get_throw_position()
            self.banana = Banana(x, y, self.gorilla2.angle, self.gorilla2.velocity, 2, 2)
            print(f"🎯 Player 2 wirft von Position ({x:.1f}, {y:.1f})")

        # Leisen Wurf-Sound abspielen
        self.throw_sound.play()

        self.waiting_for_input = False
        print("🍌 Banane wurde geworfen...")



    # In der update-Methode:
    def update(self):
        # Krater aktualisieren
        update_building_craters(self.buildings)

        if self.banana and self.banana.active:
            collision_occurred, collision_type = self.banana.update(
                self.wind, self.buildings, self.gorilla1, self.gorilla2
            )

            if collision_occurred:
                print(f"💥 Kollision aufgetreten: {collision_type}")

                if collision_type in ["player1", "player2"]:
                    self.hit_sound.play()
                    self.handle_game_over(collision_type)
                elif collision_type == "building":
                    self.building_hit_sound.play()
                    print("🏢 Gebäude getroffen! Versuche Krater zu erzeugen...")

                    # Krater an der Einschlagstelle hinzufügen
                    impact_x, impact_y = self.banana.get_impact_position()
                    print(f"🎯 Einschlagposition: ({impact_x}, {impact_y})")

                    if impact_x and impact_y:
                        success = add_crater_to_building(self.buildings, impact_x, impact_y)
                        if success:
                            print("✅ Krater erfolgreich hinzugefügt")
                        else:
                            print("❌ Krater konnte nicht hinzugefügt werden")
                    else:
                        print("❌ Keine gültige Einschlagposition")

                    self.switch_player()
                else:
                    self.switch_player()

        elif self.banana and not self.banana.active:
            self.switch_player()
    def switch_player(self):
        self.banana = None
        self.current_player = 3 - self.current_player  # 1 -> 2, 2 -> 1
        self.wind = random.uniform(-3.0, 3.0)
        self.waiting_for_input = True
        print(f"🔄 Spielerwechsel zu Player {self.current_player}")
        print(f"🌬️  Neuer Wind: {self.wind:.1f}")

    def handle_game_over(self, collision_type):
        winner = 2 if collision_type == "player1" else 1

        if winner == 1:
            self.score1 += 1
        else:
            self.score2 += 1

        print(f"🏆 Player {winner} gewinnt! Stand: P1 {self.score1} - P2 {self.score2}")
        self.show_game_over_screen(winner)
        self.restart_round()

    def show_game_over_screen(self, winner):
        self.screen.fill((0, 0, 0))
        text = self.font.render(f"Player {winner} gewinnt die Runde!", True, (255, 255, 255))
        screen_width, screen_height = self.screen.get_size()
        self.screen.blit(text, (screen_width // 2 - 100, screen_height // 2 - 20))

        score_text = self.font.render(f"Score: P1 {self.score1} - P2 {self.score2}", True, (255, 255, 255))
        self.screen.blit(score_text, (screen_width // 2 - 80, screen_height // 2 + 20))

        pygame.display.flip()
        pygame.time.delay(2000)

    def restart_round(self):
        self.buildings = generate_buildings()

        # KORREKTUR: Positionen erneut basierend auf neuen Gebäuden setzen
        first_building = self.buildings[0]
        last_building = self.buildings[-1]

        self.gorilla1.x = first_building["rect"].centerx
        self.gorilla1.y = first_building["rect"].top - GORILLA_SIZE
        self.gorilla2.x = last_building["rect"].centerx
        self.gorilla2.y = last_building["rect"].top - GORILLA_SIZE

        self.banana = None
        self.gorilla1.angle = 45
        self.gorilla1.velocity = 25
        self.gorilla2.angle = 45
        self.gorilla2.velocity = 25
        self.waiting_for_input = True
        self.wind = random.uniform(-3.0, 3.0)

        # Startspieler für nächste Runde wechseln
        self.round_count += 1
        if self.round_count % 2 == 1:
            self.current_player = 1
            print(f"🔄 Runde {self.round_count}: Player 1 (ROT) beginnt!")
        else:
            self.current_player = 2
            print(f"🔄 Runde {self.round_count}: Player 2 (BLAU) beginnt!")

        print(f"   Player 1 neue Position: ({self.gorilla1.x:.1f}, {self.gorilla1.y:.1f})")
        print(f"   Player 2 neue Position: ({self.gorilla2.x:.1f}, {self.gorilla2.y:.1f})")