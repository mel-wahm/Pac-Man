import arcade
import json

from ..config import THEMES, keys
from ..core import Directions
from ..engine import GameEngine, AudioEngine
from .ingame_settings_view import InGameSettings
from .leaderboard_view import Board


class Text:
    def __init__(self, cx, cy):
        self.cx = cx
        self.cy = cy
        self.name = ""
        white = arcade.color.WHITE
        self.text_name = arcade.Text(
            self.name,
            cx,
            cy,
            white,
            32,
            anchor_x="center",
            font_name="Renogare",
        )
        self.path = "Src/config/leaderboard.json"

    def update_text(self):
        white = arcade.color.WHITE
        self.text_name = arcade.Text(
            self.name,
            self.cx,
            self.cy,
            white,
            32,
            anchor_x="center",
            font_name="Renogare",
        )

    def on_text(self, key):
        if key.isalnum() and len(self.name) < 10:
            self.name += key
            self.update_text()

    def on_finish(self, score):
        if self.name.strip():
            Board.update_json(self.path, self.name, score)
            return 1
        return 0


class Game(arcade.View):
    def __init__(self, maze: list, screen_view):
        super().__init__()
        self.audio_engine = AudioEngine()
        with open("Src/config/audio_and_theme.json") as f:
            ant_dict = json.load(f)
        self.volume = ant_dict["volume"] / 10
        self.theme = ant_dict["theme"]
        self.music_player = None
        self.screen_view = screen_view
        self.theme = self.theme if self.theme in THEMES else "dark"
        self.theme_colors = THEMES.get(self.theme, THEMES["dark"])
        self.background_color = self.theme_colors["background"]
        cx = self.width / 2
        cy = self.height / 2

        # View and Layout Configuration
        sidebar_width = 170
        padding = 20
        self.cols = len(maze[0])
        self.rows = len(maze)
        self.half_width = (self.cols - 1) / 2
        self.half_height = (self.rows - 1) / 2
        available_width = self.width - sidebar_width - padding
        available_height = self.height - padding
        self.cell_size = min(
            available_width / self.cols, available_height / self.rows
        )
        self.wall_thickness = max(1, int(self.cell_size * 0.03))
        self.enter_text = arcade.Text(
            "Please enter your name for the highscore",
            cx,
            cy + 100,
            (80, 80, 80, 180),
            32,
            anchor_x="center",
            font_name="Renogare",
        )
        self.sec = 0

        # Initialize Game Engine
        self.engine = GameEngine(
            maze, self.center, self.cell_size, theme=self.theme
        )

        # UI & Fonts
        arcade.load_font("fonts/Renogare-Regular.otf")

        self.pause_text = arcade.Text(
            "PAUSE",
            cx,
            cy,
            self.theme_colors["pause_text"],
            font_size=160,
            anchor_x="center",
            anchor_y="center",
            font_name="Renogare",
        )
        self.won_text = arcade.Text(
            "YOU WON",
            cx,
            cy,
            self.theme_colors["won_text"],
            font_size=280,
            anchor_x="center",
            anchor_y="center",
            font_name="Renogare",
        )
        self.on_name = False
        self.text = Text(self.center_x, self.center_y)

        self.pointer_text = arcade.Text(
            "|",
            self.text.text_name.right + 5,
            cy,
            (80, 80, 80, 180),
            32,
            anchor_x="center",
            font_name="Renogare",
        )

    @property
    def progress(self):
        return self.engine.progress

    def back_to_menu(self):
        self.window.show_view(self.screen_view)

    def on_text(self, text):
        if self.on_name:
            self.text.on_text(text)

    def toggle_theme(self, new_theme):
        self.theme = new_theme if new_theme in THEMES else "dark"
        self.theme_colors = THEMES.get(self.theme, THEMES["dark"])
        self.background_color = self.theme_colors["background"]
        self.pause_text.color = self.theme_colors["pause_text"]
        self.won_text.color = self.theme_colors["won_text"]
        self.engine.pacman.score_text.color = self.theme_colors["hud_text"]
        self.engine.pacman.lives_text.color = self.theme_colors["hud_text"]
        self.engine.time_text.color = self.theme_colors["hud_text"]
        ghost_colors = self.theme_colors["ghosts"]
        for i, ghost in enumerate(self.engine.ghosts):
            ghost.color = ghost_colors[i % len(ghost_colors)]
        for dot in self.engine.dots:
            if isinstance(dot, arcade.SpriteCircle):
                dot.color = self.theme_colors["dot"]

    def on_show_view(self):
        if self.music_player is None:
            self.music_player = self.audio_engine.music.play(
                self.volume, loop=True
            )
        elif not self.music_player.playing:
            self.music_player.play()

    def on_hide_view(self):
        if self.music_player and self.music_player.playing:
            self.music_player.pause()

    def center(self, grid_x, grid_y):
        sidebar_width = 170
        padding = 20
        cx = sidebar_width + (self.width - sidebar_width - padding) / 2
        cy = self.height / 2

        screen_x = cx + (grid_x - self.half_width) * self.cell_size
        screen_y = cy - (grid_y - self.half_height) * self.cell_size
        return (screen_x, screen_y)

    def reset_game(self):
        self.engine.reset_game()
        self.won_text.font_size = 280

    def on_key_press(self, symbol, modifiers):
        if self.engine.state == 1:
            if symbol == arcade.key.ENTER:
                if self.text.on_finish(self.engine.pacman.final_score):
                    self.on_name = False
                    self.back_to_menu()
            if symbol == arcade.key.BACKSPACE:
                if self.text.name:
                    self.text.name = self.text.name[:-1]
                    self.text.update_text()
            return
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
        self.pointer_text.x = self.text.text_name.right + 7
        if self.engine.state == 1:
            if self.sec > 1.5:
                self.sec = 0
            self.sec += delta_time
        if self.engine.state == 3:
            t = self.engine.win_timer
            ease_out = t * (2 - t)
            self.won_text.font_size = int(280 - (280 - 60) * ease_out)

    def on_draw(self):
        self.clear()

        # Draw Walls (Outer Outline + Inner Core)
        if self.engine.wall_lines:
            outer_thickness = max(4, int(self.wall_thickness * 2.2))
            wall_outline_col = self.theme_colors.get(
                "wall_outline", self.theme_colors["wall"]
            )
            arcade.draw_lines(
                self.engine.wall_lines,
                wall_outline_col,
                outer_thickness,
            )
            arcade.draw_lines(
                self.engine.wall_lines,
                self.theme_colors["wall"],
                self.wall_thickness,
            )

        # Draw Dots & Super Gums
        self.engine.dots.draw()

        # Draw 42 Center Blocks (Outer Outline + Inner Core)
        block_outline_col = self.theme_colors.get(
            "center_block_outline", self.theme_colors["wall_outline"]
        )
        for c, r in self.engine.forty_two_coords:
            real_x, real_y = self.center(c, r)
            sqr_outer = arcade.rect.XYWH(
                real_x,
                real_y,
                self.cell_size * 0.54,
                self.cell_size * 0.54,
            )
            arcade.draw_rect_filled(sqr_outer, block_outline_col)
            sqr = arcade.rect.XYWH(
                real_x,
                real_y,
                self.cell_size * 0.44,
                self.cell_size * 0.44,
            )
            arcade.draw_rect_filled(sqr, self.theme_colors["center_block"])

        # Draw Pac-Man and Ghosts
        self.engine.pacman.draw(self)
        for ghost in self.engine.ghosts:
            if not ghost.eaten_timer:
                ghost.draw(self.theme_colors)

        # Draw Sidebar HUD (Score & Lives)
        sidebar_x = 20
        self.engine.pacman.score_text.draw()
        self.engine.pacman.lives_text.draw()
        self.engine.time_text.draw()

        lives_remaining = 3 - self.engine.pacman.death_count
        for i in range(lives_remaining):
            arcade.draw_arc_filled(
                sidebar_x + 20 + (i * 45),
                self.height - 230,
                32,
                32,
                self.theme_colors["pacman"],
                30,
                330,
            )

        # Draw State Overlays (Pause / Died / Won)
        if self.engine.pause:
            cx = self.width / 2
            cy = self.height / 2
            shade = arcade.rect.XYWH(cx, cy, self.width, self.height)
            arcade.draw_rect_filled(shade, self.theme_colors["dim_overlay"])
            if self.engine.state == 1:
                self.on_name = True
                r = arcade.rect.XYWH(cx, cy, self.width, self.height)
                arcade.draw_rect_filled(r, (10, 10, 10, 200))
                self.enter_text.draw()
                self.text.text_name.draw()
                if self.sec < 0.75:
                    self.pointer_text.draw()

            if self.engine.state == 2:
                self.pause_text.draw()
            if self.engine.state == 3:
                self.won_text.draw()
