# NOKIA SNAKE 🐍

**Pure ASCII terminal Snake game** — Authentic Nokia experience in your terminal. No deps, no BS. Full TUI, wrap-around movement, speed control, high score tracking.

```
SCORE:   150  LEVEL: 2  HIGH:   480  SPEED: NORMAL

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                                                                      ┃
┃                    ●●●                                              ┃
┃                       ◆                                             ┃
┃                                                                      ┃
┃                                                                      ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

↑↓←→=Move  ESC=Pause
```

---

## ✨ Features

✅ **Fills your terminal** — Game area scales to window size  
✅ **Wrap-around movement** — Go off edge, come out the other side (true Nokia!)  
✅ **4 speed levels** — Slow (200ms) → Crazy (40ms)  
✅ **Pause & resume** — ESC to pause, continue where you left off  
✅ **High score persistence** — Automatically saved  
✅ **Menu system** — Main menu with all options  
✅ **Level progression** — Increases per 100 points  
✅ **Pure Python** — No external dependencies, just curses (stdlib)  

---

## 🎮 How to Play

### Start Game
```bash
python3 nokia_snake.py
```

### Controls

| Action | Key |
|--------|-----|
| Move up | `↑` Arrow Up |
| Move down | `↓` Arrow Down |
| Move left | `←` Arrow Left |
| Move right | `→` Arrow Right |
| Pause | `ESC` |

### Pause Menu
| Action | Key |
|--------|-----|
| Resume | `R` |
| Main Menu | `M` |
| Quit | `Q` |

### Game Over
| Action | Key |
|--------|-----|
| New Game | `N` |
| Main Menu | `M` |
| Quit | `Q` |

### Main Menu
| Action | Key |
|--------|-----|
| Navigate | `↑` `↓` |
| Select | `ENTER` |
| Back/Exit | `ESC` |

---

## 🎯 Game Rules

**Eat food (◆)**
- +10 points per food
- Snake grows by 1
- New food spawns randomly

**Level System**
- Level 1 → Level 2 at 100 points
- Level 2 → Level 3 at 200 points
- etc.

**Game Over**
- Hit yourself (self-collision)
- That's it! No wall collisions with wrap-around.

**Wrap-Around**
- Go off the left edge → appear on the right
- Go off the top → appear at the bottom
- Go off any edge → wrap to opposite side (authentic Nokia behavior)

---

## ⚙️ Speed Levels

| Level | Delay | Feel | Best For |
|-------|-------|------|----------|
| **SLOW** | 200ms | Relaxed, chill | Learning, kids |
| **NORMAL** | 120ms | Default difficulty | Most players |
| **FAST** | 80ms | Challenge | Experienced |
| **CRAZY** | 40ms | Hardcore | Speedrunners |

Change speed from **Main Menu → SPEED** before starting a game.

---

## 📊 Gameplay Flow

```
┌─────────────────┐
│  Title Screen   │
│ PRESS ENTER    │
└────────┬────────┘
         │
    ┌────▼─────────────────────┐
    │    Main Menu              │
    │ • New Game               │
    │ • Continue* (if paused)  │
    │ • Speed                  │
    │ • Exit                   │
    └────┬──────────────┬───┬──┘
         │              │   │
      Game         Speed    Exit
         │          Menu
         │
    ┌────▼──────────────┐
    │  Playing...        │
    │ ESC to pause      │
    │                   │
    │ ●●● ◆            │
    └────┬──────────────┘
         │ ESC
    ┌────▼──────────────┐
    │  Pause Menu       │
    │ R=Resume          │
    │ M=Menu            │
    │ Q=Quit            │
    └──────────────────┘
         or (game over)
    ┌────▼──────────────┐
    │  Game Over        │
    │ Score: 150        │
    │ N=New M=Menu Q=Quit│
    └──────────────────┘
```

---

## 📝 Files & Storage

**Main Game File**
- `nokia_snake.py` — Entire game (single file, ~500 lines)

**High Score Storage**
- `~/.nokia_snake_highscore` — Auto-created JSON file
- Survives restarts
- Format: `{"high_score": 480}`

---

## 🛠️ Installation

### Requirements
- Python 3.x
- `curses` (built-in on Linux/macOS)
- Terminal that supports ANSI colors (all modern ones do)

### For Windows
Use **WSL (Windows Subsystem for Linux)** or **Git Bash**.
Native Windows `cmd.exe` doesn't support curses.

### Quick Setup
```bash
# Clone or copy nokia_snake.py to your folder
cd ascii-forge/tools/nokia_snake/

# Make executable (Linux/macOS)
chmod +x nokia_snake.py

# Run
python3 nokia_snake.py
```

---

## 🎨 Colors & Styling

| Element | Color |
|---------|-------|
| Snake head (●) | Bright white |
| Snake body (●) | Green |
| Food (◆) | Red |
| Borders | Yellow |
| Text | White |
| Background | Black |

---

## 🔧 Customization

Edit `nokia_snake.py` to change game parameters:

```python
# At the top of the file:
SPEED_LEVELS = {
    "SLOW": 200,       # milliseconds per move
    "NORMAL": 120,
    "FAST": 80,
    "CRAZY": 40
}

HIGH_SCORE_FILE = os.path.expanduser("~/.nokia_snake_highscore")
```

Add new speed levels by adding entries to `SPEED_LEVELS` dict.

---

## 🐛 Troubleshooting

**Game won't start on Windows**
- Use WSL or Git Bash, not cmd.exe
- `curses` requires Unix-like environment

**Terminal too small**
- Resize your terminal window
- Minimum: ~60 cols × 25 rows recommended

**Game feels slow/laggy**
- Increase speed in Speed menu
- Or check terminal performance (some terminals are slower)

**High score not saving**
- Check write permissions in home directory
- Make sure `~/.nokia_snake_highscore` isn't read-only

**Colors look wrong**
- Verify your terminal supports 256 colors
- Try a different terminal (xterm, kitty, alacritty all work)

---

## 📈 Tips & Tricks

**Score Fast**
- Play on FAST/CRAZY speed
- Each food = 10 points
- Levels increase per 100 points

**Wrap-Around Strategy**
- Use edges to quickly reposition
- Don't trap yourself in corners!

**Marathon Strategy**
- Play SLOW for longest game
- Build long snake carefully

**High Score Record**
- Current best: *Your turn to beat it!* 🏆

---

## 🎓 How It Works

**Game Loop** (~60 FPS, 16ms per frame)
1. Capture input (arrow keys, ESC)
2. Every `speed_ms` milliseconds → move snake
3. Check collisions
4. Spawn food on eat
5. Render to terminal
6. Repeat

**Wrap-Around Math**
```python
new_x = (head_x + dx) % width   # Modulo wrapping
new_y = (head_y + dy) % height
```

**Non-Blocking Input**
- Terminal set to `nodelay(True)`
- Doesn't freeze waiting for key presses
- Smooth, responsive controls

---

## 🚀 Running from anywhere

**Add to PATH (Linux/macOS)**
```bash
# Copy to /usr/local/bin
sudo cp nokia_snake.py /usr/local/bin/nokia-snake
sudo chmod +x /usr/local/bin/nokia-snake

# Now run from anywhere:
nokia-snake
```

**Create alias**
```bash
# Add to ~/.bashrc or ~/.zshrc
alias snake='python3 ~/path/to/nokia_snake.py'

# Then:
snake
```

---

## 📜 License

MIT — Free to use, modify, share.

---

## 🎮 Have Fun!

Try to beat the high score. Push the speed. Master wrap-around.

**Game created for ascii-forge** — Pure terminal tools, no deps.

```
╔════════════════════════════════════════════╗
║                                            ║
║      Thanks for playing NOKIA SNAKE!      ║
║                                            ║
║        Can you beat the high score?        ║
║                                            ║
╚════════════════════════════════════════════╝
```

---

**Commands Quick Reference**
```
Start:        python3 nokia_snake.py
Move:         Arrow Keys
Pause:        ESC
Menu:         ENTER to select, ↑↓ to navigate
Speed:        Set in Main Menu before game
Exit:         Q from Game Over, ESC from menu
High Score:   Automatically saved & loaded
```
