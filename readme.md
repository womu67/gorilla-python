```markdown
# 🦍 Gorillas Python Game

Ein Python-Implementierung des klassischen Gorillas-Spiels, bei dem zwei Gorillas sich mit Bananen auf Hochhäusern bekämpfen. Inspiriert vom originalen QBasic Gorillas Spiel.

![Gorillas Game Screenshot](screenshot.png)

## 🎮 Über das Spiel

Zwei Gorillas stehen auf Hochhäusern und werfen sich Bananen zu. Das Ziel ist es, den gegnerischen Gorilla mit einer Banane zu treffen, während Wind und Physik die Flugbahn beeinflussen.

### Features
- 🏢 Zufällig generierte Hochhaus-Skyline
- 💨 Dynamischer Wind mit Einfluss auf die Flugbahn
- 🕳️ Echte Krater in Gebäuden (Bananen fliegen durch Löcher)
- 🎨 Detaillierte Gorilla-Grafiken mit Animationen
- 🔊 Sound-Effekte für Würfe und Treffer
- 🏆 Punktesystem mit Rundenwechsel

## 🚀 Installation

### Voraussetzungen
- Python 3.7 oder höher
- Pygame-Bibliothek

### Installation
1. Repository klonen:
```bash
git clone https://github.com/dein-username/gorillas-python.git
cd gorillas-python
```

2. Pygame installieren:
```bash
pip install pygame
```

3. Gorilla-Bilder erstellen:
```bash
python create_gorilla_images.py
```

4. Spiel starten:
```bash
python Main.py
```

## 🎯 Steuerung

### Player 1 (Links, Roter Gorilla)
- **W/S** - Winkel ändern (0-90°)
- **A/D** - Geschwindigkeit ändern (10-80)
- **LEERTASTE** - Banane werfen

### Player 2 (Rechts, Blauer Gorilla)
- **PFEIL HOCH/RUNTER** - Winkel ändern (0-90°)
- **PFEIL LINKS/RECHTS** - Geschwindigkeit ändern (10-80)
- **ENTER** - Banane werfen

## 🏗️ Projektstruktur

```
gorillas-python/
├── assets/                 # Grafiken und Sounds
│   ├── gorilla1.png       # Roter Gorilla (normal)
│   ├── gorilla1_throw.png # Roter Gorilla (werfend)
│   ├── gorilla2.png       # Blauer Gorilla (normal)
│   └── gorilla2_throw.png # Blauer Gorilla (werfend)
├── Main.py                # Hauptprogramm
├── game_logic.py          # Spiel-Logik
├── gorillas.py            # Gorilla-Klasse
├── banana.py              # Bananen-Physik
├── buildings.py           # Gebäude und Krater
├── ui.py                  # Benutzeroberfläche
├── config.py              # Konfiguration und Einstellungen
├── create_gorilla_images.py # Bild-Generator
└── README.md              # Diese Datei
```

## 🔧 Technische Details

### Physik-Engine
- Realistische Flugbahn-Berechnung mit Gravitation
- Wind-Einfluss auf die Bananen
- Kollisionserkennung für Gebäude und Gorillas

### Grafik-System
- Automatische Generierung von Gorilla-Bildern
- Dynamische Gebäude-Generierung
- Animierte Wurf-Bewegungen
- Permanente Krater in Gebäuden

### Sound-System
- Generierte Sound-Effekte für:
  - Bananenwurf
  - Gebäude-Treffer
  - Gorilla-Treffer

## 🎨 Anpassungen

### Schwierigkeit anpassen
In `config.py` können folgende Werte geändert werden:
```python
GRAVITY = 0.5              # Schwerkraft anpassen
WIND_RANGE = (-3.0, 3.0)   # Wind-Stärke
BUILDING_WIDTH = 60        # Gebäude-Breite
```

### Grafiken anpassen
Führe `create_gorilla_images.py` erneut aus oder ersetze die PNG-Dateien im `assets/` Ordner.

## 🤝 Beitragen

Beiträge sind willkommen! Folgende Bereiche könnten erweitert werden:
- Mehr Power-Ups und Spezialfähigkeiten
- Level-Editor für Gebäude
- Online-Multiplayer
- Bestenlisten

## 📜 Lizenz

Dieses Projekt steht unter der MIT-Lizenz. Siehe [LICENSE](LICENSE) Datei für Details.

## 🙏 Danksagung

Inspiriert vom originalen Gorillas-Spiel von IBM aus den 1990er Jahren.

---

**Viel Spaß beim Spielen!** 🦍🍌🎯
```

## Zusätzlich empfohlen:

**Erstelle eine `requirements.txt` Datei:**
```txt
pygame==2.5.1
```

**Und eine `.gitignore` Datei:**
```gitignore
# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
pip-log.txt

# PyGame
*.save
*.sav

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
```

**Für ein Screenshot** könntest du während des Spiels mit `F12` oder `Print Screen` einen Screenshot machen und als `screenshot.png` speichern.

Die README ist jetzt professionell genug für GitHub und gibt anderen Entwicklern einen guten Überblick über dein Projekt! 🚀