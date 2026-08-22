import arcade

from ..config import keys
from ..core import Directions
from ..engine import GameEngine
from .ingame_settings_view import InGameSettings


class Game(arcade.View):
    def __init__(self, maze: list, screen_view):
        super().__init__()

        self.screen_view = screen_view
        self.background_color = (20, 20, 30)

        # View and Layout Configuration
        sidebar_width = 170
        padding = 20
        self.cols = len(maze[0])
        self.rows = len(maze)
        self.half_width = (self.cols - 1) / 2
        self.half_height = (self.rows - 1) / 2
        available_width = self.width - sidebar_width - padding
        available_height = self.height - padding
        self.cell_size = min(available_width / self.cols, available_height / self.rows)
        self.wall_thickness = max(1, int(self.cell_size * 0.03))

        # Initialize Game Engine
        self.engine = GameEngine(maze, self.center, self.cell_size)

        # UI & Fonts
        arcade.load_font("fonts/Renogare-Regular.otf")
        center_x = self.width / 2
        center_y = self.height / 2

        self.pause_text = arcade.Text(
            "PAUSE",
            center_x,
            center_y,
            (200, 200, 200),
            font_size=160,
            anchor_x="center",
            anchor_y="center",
            font_name="Renogare",
        )
        self.died_text = arcade.Text(
            "YOU DIED",
            center_x,
            center_y,
            (180, 15, 15),
            font_size=80,
            anchor_x="center",
            anchor_y="center",
            font_name="Renogare",
        )
        self.won_text = arcade.Text(
            "YOU WON",
            center_x,
            center_y,
            (255, 200, 0),
            font_size=280,
            anchor_x="center",
            anchor_y="center",
            font_name="Renogare",
        )

    @property
    def progress(self):
        return self.engine.progress

    def center(self, grid_x, grid_y):
        sidebar_width = 170
        padding = 20
        center_x = sidebar_width + (self.width - sidebar_width - padding) / 2
        center_y = self.height / 2

        screen_x = center_x + (grid_x - self.half_width) * self.cell_size
        screen_y = center_y - (grid_y - self.half_height) * self.cell_size
        return (screen_x, screen_y)

    def reset_game(self):
        self.engine.reset_game()
        self.won_text.font_size = 280

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.C and modifiers & arcade.key.MOD_CTRL:
            exit()
        if symbol == keys["UP"]:
            self.engine.pacman.set_next_direction(Directions.UP)
        if symbol == keys["DOWN"]:
            self.engine.pacman.set_next_direction(Directions.DOWN)
        if symbol == keys["RIGHT"]:
            self.engine.pacman.set_next_direction(Directions.RIGHT)
        if symbol == keys["LEFT"]:
            self.engine.pacman.set_next_direction(Directions.LEFT)
        if symbol == arcade.key.ESCAPE:
            set_view = InGameSettings(self, self.screen_view)
            self.window.show_view(set_view)
        if symbol == arcade.key.SPACE:
            self.engine.state = 2
            self.engine.pause = not (self.engine.pause)

    def on_update(self, delta_time):
        self.engine.update(delta_time)

        if self.engine.state == 3:
            t = self.engine.win_timer
            ease_out = t * (2 - t)
            self.won_text.font_size = int(280 - (280 - 60) * ease_out)

    def on_draw(self):
        self.clear()

        # Draw Walls
        if self.engine.wall_lines:
            arcade.draw_lines(
                self.engine.wall_lines, (33, 33, 255), self.wall_thickness
            )

        # Draw Dots & Super Gums
        self.engine.dots.draw()

        # Draw 42 Center Blocks
        for c, r in self.engine.forty_two_coords:
            real_x, real_y = self.center(c, r)
            sqr = arcade.rect.XYWH(
                real_x,
                real_y,
                self.cell_size * 0.5,
                self.cell_size * 0.5,
            )
            arcade.draw_rect_filled(sqr, (33, 33, 255))

        # Draw Pac-Man and Ghosts
        self.engine.pacman.draw(self)
        for ghost in self.engine.ghosts:
            if not ghost.eaten_timer:
                ghost.draw()

        # Draw Sidebar HUD (Score & Lives)
        sidebar_x = 20
        self.engine.pacman.score_text.x = sidebar_x
        self.engine.pacman.score_text.y = self.height - 100
        self.engine.pacman.score_text.draw()
        self.engine.pacman.lives_text.x = sidebar_x
        self.engine.pacman.lives_text.y = self.height - 170
        self.engine.pacman.lives_text.draw()

        lives_remaining = 3 - self.engine.pacman.death_count
        for i in range(lives_remaining):
            arcade.draw_arc_filled(
                sidebar_x + 20 + (i * 45),
                self.height - 230,
                32,
                32,
                arcade.color.YELLOW,
                30,
                330,
            )

        # Draw State Overlays (Pause / Died / Won)
        if self.engine.pause:
            cx = self.width / 2
            cy = self.height / 2
            shade = arcade.rect.XYWH(cx, cy, self.width, self.height)
            arcade.draw_rect_filled(shade, (10, 10, 10, 170))
            if self.engine.state == 1:
                self.died_text.draw()
            if self.engine.state == 2:
                self.pause_text.draw()
            if self.engine.state == 3:
                self.won_text.draw()
