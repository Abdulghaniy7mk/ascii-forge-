#!/usr/bin/env python3
"""
NOKIA SNAKE - Terminal Edition
Pure ASCII, full TUI, fills terminal, wrap-around, speed control.
"""

import curses
import random
import json
import os
import time
from collections import deque
from enum import Enum

HIGH_SCORE_FILE = os.path.expanduser("~/.nokia_snake_highscore")

SPEED_LEVELS = {
    "SLOW": 200,
    "NORMAL": 120,
    "FAST": 80,
    "CRAZY": 40
}

class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

# ============================================================================
# COLOR SETUP
# ============================================================================

def setup_colors():
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_WHITE)

# ============================================================================
# GAME STATE
# ============================================================================

class GameState:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.reset()
        self.high_score = self.load_high_score()
        self.speed_name = "NORMAL"
        self.speed_ms = SPEED_LEVELS["NORMAL"]

    def reset(self):
        """Reset game to starting state."""
        self.snake = deque([
            (self.width // 2, self.height // 2),
            (self.width // 2 - 1, self.height // 2),
            (self.width // 2 - 2, self.height // 2),
        ])
        self.direction = Direction.RIGHT
        self.next_direction = Direction.RIGHT
        self.food = self.spawn_food()
        self.score = 0
        self.level = 1

    def spawn_food(self):
        """Spawn food at random location not on snake."""
        while True:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if (x, y) not in self.snake:
                return (x, y)

    def load_high_score(self):
        if os.path.exists(HIGH_SCORE_FILE):
            try:
                with open(HIGH_SCORE_FILE, 'r') as f:
                    data = json.load(f)
                    return data.get('high_score', 0)
            except:
                return 0
        return 0

    def save_high_score(self):
        try:
            with open(HIGH_SCORE_FILE, 'w') as f:
                json.dump({'high_score': self.high_score}, f)
        except:
            pass

    def update_high_score(self):
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()

# ============================================================================
# RENDERING
# ============================================================================

class Renderer:
    def __init__(self, stdscr, game_state):
        self.stdscr = stdscr
        self.game = game_state

    def clear(self):
        try:
            self.stdscr.clear()
        except:
            pass

    def refresh(self):
        try:
            self.stdscr.refresh()
        except:
            pass

    def draw_title(self):
        self.clear()
        self.stdscr.attron(curses.color_pair(5))
        
        lines = [
            "╔════════════════════════════════════════════════╗",
            "║                                                ║",
            "║           ██╗ ██╗ ██████╗ ██╗  ██╗███╗   ███╗║",
            "║           ██║ ██║██╔═══██╗██║ ██╔╝████╗ ████║║",
            "║           ██║ ██║██║   ██║█████╔╝ ██╔████╔██║║",
            "║           ╚██╗██╔╝██║   ██║██╔═██╗ ██║╚██╔╝██║║",
            "║            ╚████╔╝ ╚██████╔╝██║  ██╗██║ ╚═╝ ██║║",
            "║             ╚═══╝   ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝║",
            "║                                                ║",
            "║                   S N A K E                    ║",
            "║                                                ║",
            "║            Press ENTER to start               ║",
            "║                                                ║",
            "╚════════════════════════════════════════════════╝",
        ]
        
        height = len(lines)
        start_y = max(0, (curses.LINES - height) // 2)
        
        for i, line in enumerate(lines):
            if start_y + i < curses.LINES:
                try:
                    self.stdscr.addstr(start_y + i, max(0, (curses.COLS - len(line)) // 2), line)
                except:
                    pass
        
        self.stdscr.attroff(curses.color_pair(5))
        self.refresh()

    def draw_menu(self, items, selected, title="MENU"):
        self.clear()
        
        self.stdscr.attron(curses.color_pair(5))
        title_line = f"╔ {title.center(20)} ╗"
        try:
            self.stdscr.addstr(2, max(0, (curses.COLS - len(title_line)) // 2), title_line)
        except:
            pass
        
        for i, label in enumerate(items):
            y = 5 + i
            if i == selected:
                self.stdscr.attron(curses.color_pair(6) | curses.A_BOLD)
                try:
                    self.stdscr.addstr(y, 10, f"  {label}  ")
                except:
                    pass
                self.stdscr.attroff(curses.color_pair(6) | curses.A_BOLD)
            else:
                self.stdscr.attron(curses.color_pair(1))
                try:
                    self.stdscr.addstr(y, 10, f"  {label}  ")
                except:
                    pass
                self.stdscr.attroff(curses.color_pair(1))
        
        self.stdscr.attron(curses.color_pair(1))
        try:
            self.stdscr.addstr(curses.LINES - 2, 2, "↑↓=Navigate  ENTER=Select  ESC=Back")
        except:
            pass
        self.stdscr.attroff(curses.color_pair(1))
        self.stdscr.attroff(curses.color_pair(5))
        
        self.refresh()

    def draw_game(self):
        self.clear()
        self.draw_hud()
        self.draw_area()
        self.draw_snake()
        self.draw_food()
        self.refresh()

    def draw_hud(self):
        self.stdscr.attron(curses.color_pair(1))
        hud = f"SCORE: {self.game.score:5d}  LEVEL: {self.game.level}  HIGH: {self.game.high_score:5d}  SPEED: {self.game.speed_name}"
        try:
            self.stdscr.addstr(0, 0, hud[:curses.COLS-1])
            self.stdscr.addstr(curses.LINES - 1, 0, "↑↓←→=Move  ESC=Pause"[:curses.COLS-1])
        except:
            pass
        self.stdscr.attroff(curses.color_pair(1))

    def draw_area(self):
        """Draw game area border (fills terminal)."""
        self.stdscr.attron(curses.color_pair(5))
        
        # Top border
        try:
            for x in range(curses.COLS):
                self.stdscr.addstr(1, x, "━")
        except:
            pass
        
        # Bottom border
        try:
            for x in range(curses.COLS):
                self.stdscr.addstr(curses.LINES - 2, x, "━")
        except:
            pass
        
        # Left & right borders
        for y in range(2, curses.LINES - 2):
            try:
                self.stdscr.addstr(y, 0, "┃")
                self.stdscr.addstr(y, curses.COLS - 1, "┃")
            except:
                pass
        
        # Corners
        try:
            self.stdscr.addstr(1, 0, "┏")
            self.stdscr.addstr(1, curses.COLS - 1, "┓")
            self.stdscr.addstr(curses.LINES - 2, 0, "┗")
            self.stdscr.addstr(curses.LINES - 2, curses.COLS - 1, "┛")
        except:
            pass
        
        self.stdscr.attroff(curses.color_pair(5))

    def draw_snake(self):
        snake_list = list(self.game.snake)
        for i, (x, y) in enumerate(snake_list):
            screen_x = 1 + x
            screen_y = 2 + y
            
            # Bounds check
            if screen_x < 1 or screen_x >= curses.COLS - 1 or screen_y < 2 or screen_y >= curses.LINES - 2:
                continue
            
            if i == 0:  # Head
                self.stdscr.attron(curses.color_pair(3) | curses.A_BOLD)
                try:
                    self.stdscr.addstr(screen_y, screen_x, "●")
                except:
                    pass
                self.stdscr.attroff(curses.color_pair(3) | curses.A_BOLD)
            else:  # Body
                self.stdscr.attron(curses.color_pair(2))
                try:
                    self.stdscr.addstr(screen_y, screen_x, "●")
                except:
                    pass
                self.stdscr.attroff(curses.color_pair(2))

    def draw_food(self):
        x, y = self.game.food
        screen_x = 1 + x
        screen_y = 2 + y
        
        if screen_x < 1 or screen_x >= curses.COLS - 1 or screen_y < 2 or screen_y >= curses.LINES - 2:
            return
        
        self.stdscr.attron(curses.color_pair(4) | curses.A_BOLD)
        try:
            self.stdscr.addstr(screen_y, screen_x, "◆")
        except:
            pass
        self.stdscr.attroff(curses.color_pair(4) | curses.A_BOLD)

    def draw_pause(self):
        self.draw_game()
        self.stdscr.attron(curses.color_pair(5))
        
        lines = [
            "┌──────────────────┐",
            "│   PAUSED         │",
            "│                  │",
            "│  R = Resume      │",
            "│  M = Menu        │",
            "│  Q = Quit        │",
            "└──────────────────┘",
        ]
        
        start_y = max(2, curses.LINES // 2 - 4)
        start_x = max(1, curses.COLS // 2 - 10)
        
        for i, line in enumerate(lines):
            try:
                self.stdscr.addstr(start_y + i, start_x, line)
            except:
                pass
        
        self.stdscr.attroff(curses.color_pair(5))
        self.refresh()

    def draw_gameover(self):
        self.clear()
        
        self.stdscr.attron(curses.color_pair(5))
        
        lines = [
            "╔──────────────────────╗",
            "║    GAME OVER!        ║",
            "║                      ║",
            f"║  SCORE: {self.game.score:5d}       ║",
            f"║  HIGH:  {self.game.high_score:5d}       ║",
            f"║  LEVEL: {self.game.level}           ║",
            "║                      ║",
            "║  N=New  M=Menu  Q=Quit║",
            "║                      ║",
            "╚──────────────────────╝",
        ]
        
        start_y = max(0, curses.LINES // 2 - len(lines) // 2)
        start_x = max(0, curses.COLS // 2 - 12)
        
        for i, line in enumerate(lines):
            try:
                self.stdscr.addstr(start_y + i, start_x, line)
            except:
                pass
        
        self.stdscr.attroff(curses.color_pair(5))
        self.refresh()

# ============================================================================
# GAME LOGIC
# ============================================================================

class Game:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.paused_game = None
        self.last_move_time = time.time()
        
        # Dynamic sizing: fill terminal
        h = max(10, curses.LINES - 3)
        w = max(20, curses.COLS - 2)
        self.game_state = GameState(w, h)
        self.renderer = Renderer(stdscr, self.game_state)

    def run(self):
        setup_colors()
        self.stdscr.nodelay(True)
        self.stdscr.timeout(100)
        curses.curs_set(0)
        
        # Title
        self.renderer.draw_title()
        while True:
            key = self.stdscr.getch()
            if key in [ord('\n'), curses.KEY_ENTER, 10, 13]:
                break
            time.sleep(0.05)
        
        self.main_menu()

    def main_menu(self):
        items = ["▶ NEW GAME"]
        if self.paused_game:
            items.append("▶ CONTINUE")
        items.extend(["⚙ SPEED", "⏹ EXIT"])
        
        selected = 0
        
        while True:
            self.renderer.draw_menu(items, selected, "MAIN MENU")
            
            key = self.stdscr.getch()
            
            if key == curses.KEY_UP:
                selected = (selected - 1) % len(items)
            elif key == curses.KEY_DOWN:
                selected = (selected + 1) % len(items)
            elif key in [ord('\n'), curses.KEY_ENTER, 10, 13]:
                action = items[selected]
                if "NEW GAME" in action:
                    self.game_state.reset()
                    self.paused_game = None
                    self.game_loop()
                elif "CONTINUE" in action:
                    self.game_loop(resume=True)
                elif "SPEED" in action:
                    self.speed_menu()
                elif "EXIT" in action:
                    return
            elif key == 27:  # ESC
                return
            
            time.sleep(0.05)

    def speed_menu(self):
        items = [f"{name} ({ms}ms)" for name, ms in SPEED_LEVELS.items()]
        selected = 0
        
        for i, item in enumerate(items):
            if self.game_state.speed_name in item:
                selected = i
                break
        
        while True:
            self.renderer.draw_menu(items, selected, "SPEED")
            
            key = self.stdscr.getch()
            
            if key == curses.KEY_UP:
                selected = (selected - 1) % len(items)
            elif key == curses.KEY_DOWN:
                selected = (selected + 1) % len(items)
            elif key in [ord('\n'), curses.KEY_ENTER, 10, 13]:
                speed_names = list(SPEED_LEVELS.keys())
                self.game_state.speed_name = speed_names[selected]
                self.game_state.speed_ms = SPEED_LEVELS[self.game_state.speed_name]
                return
            elif key == 27:  # ESC
                return
            
            time.sleep(0.05)

    def game_loop(self, resume=False):
        """Main game loop - returns when done."""
        if not resume:
            self.game_state.reset()
        
        self.last_move_time = time.time()
        
        while True:
            key = self.stdscr.getch()
            
            if key == 27:  # ESC - pause
                self.paused_game = self.game_state
                self.pause_menu()
                return  # Return to main menu
            elif key == curses.KEY_UP:
                if self.game_state.direction != Direction.DOWN:
                    self.game_state.next_direction = Direction.UP
            elif key == curses.KEY_DOWN:
                if self.game_state.direction != Direction.UP:
                    self.game_state.next_direction = Direction.DOWN
            elif key == curses.KEY_LEFT:
                if self.game_state.direction != Direction.RIGHT:
                    self.game_state.next_direction = Direction.LEFT
            elif key == curses.KEY_RIGHT:
                if self.game_state.direction != Direction.LEFT:
                    self.game_state.next_direction = Direction.RIGHT
            
            current_time = time.time()
            if (current_time - self.last_move_time) * 1000 >= self.game_state.speed_ms:
                if self.update_game():  # Returns True if game over
                    self.game_over()
                    return  # Return to main menu
                self.last_move_time = current_time
            
            self.renderer.draw_game()
            time.sleep(0.016)

    def pause_menu(self):
        """Pause menu - returns when done."""
        while True:
            self.renderer.draw_pause()
            
            key = self.stdscr.getch()
            
            if key == ord('r') or key == ord('R'):
                return  # Resume
            elif key == ord('m') or key == ord('M'):
                self.paused_game = None
                return  # Go to main menu
            elif key == ord('q') or key == ord('Q'):
                self.paused_game = None
                return  # Quit
            
            time.sleep(0.05)

    def update_game(self):
        """Update game state. Returns True if game over."""
        self.game_state.direction = self.game_state.next_direction
        
        dx, dy = self.game_state.direction.value
        head_x, head_y = self.game_state.snake[0]
        
        # WRAP-AROUND (Nokia style!)
        new_x = (head_x + dx) % self.game_state.width
        new_y = (head_y + dy) % self.game_state.height
        new_head = (new_x, new_y)
        
        # Self collision (only thing that kills you with wrap-around)
        if new_head in self.game_state.snake:
            self.game_state.update_high_score()
            return True  # Game over
        
        self.game_state.snake.appendleft(new_head)
        
        # Food collision
        if new_head == self.game_state.food:
            self.game_state.score += 10
            self.game_state.level = 1 + (self.game_state.score // 100)
            self.game_state.food = self.game_state.spawn_food()
        else:
            self.game_state.snake.pop()
        
        return False  # Game continues

    def game_over(self):
        """Game over screen."""
        while True:
            self.renderer.draw_gameover()
            
            key = self.stdscr.getch()
            
            if key == ord('n') or key == ord('N'):
                self.game_state.reset()
                self.paused_game = None
                self.game_loop()
                return
            elif key == ord('m') or key == ord('M'):
                return
            elif key == ord('q') or key == ord('Q'):
                return
            
            time.sleep(0.05)

# ============================================================================
# MAIN
# ============================================================================

def main(stdscr):
    game = Game(stdscr)
    game.run()

if __name__ == "__main__":
    curses.wrapper(main)
