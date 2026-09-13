import json
import sys
from typing import Any

import arcade
from mazegenerator import MazeGenerator

from ..config import THEMES, keys
from ..core import Directions
from ..engine import AudioEngine, GameEngine
from .ingame_settings_view import InGameSettings
from .leaderboard_view import Board


class Text:
    """Manages player name entry text input and submission for highscores."""

    def __init__(self, cx: float, cy: float, config: dict[str, Any]) -> None:
        self.cx = cx
        self.cy = cy
        self.name = ""
        self.config = config
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
        self.path = config.get(
            "highscore_filename", "src/config/leaderboard.json"
        )

    def update_text(self) -> None:
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

    def on_text(self, key: str) -> None:
        if (key.isalnum() or key == " ") and len(self.name) < 10:
            self.name += key
            self.update_text()

    def on_finish(self, score: int) -> int:
        if self.name.strip():
            Board.update_json(self.path, self.name, score)
            self.name = ""
            self.update_text()
            return 1
        return 0


class Game(arcade.View):
    """Main gameplay view handling rendering, levels, and user inputs."""

    def __init__(self, screen_view: Any, config: dict[str, Any]) -> None:
        super().__init__()
        self.config = config
        self.audio_engine = AudioEngine()
        options_path = "src/config/options.json"
        try:
            with open(options_path) as f:
                ant_dict = json.load(f)
        except Exception:
            ant_dict = {"volume": 0, "theme": "dark"}

        self.volume = ant_dict.get("volume", 0) / 10
        self.theme = ant_dict.get("theme", "dark")
        self.music_player: Any = None
        self.screen_view = screen_view
        self.theme = self.theme if self.theme in THEMES else "dark"
        self.theme_colors = THEMES.get(self.theme, THEMES["dark"])
        self.background_color = self.theme_colors["background"]
        cx = self.width / 2
        cy = self.height / 2
        self.current_level_index = 0
        self.levels: list[dict[str, int]] = self.config.get("levels", [])
        self.mazes: list[list[list[int]]] = []

        for idx, lvl in enumerate(self.levels):
            lvl_seed = (
                self.config["seed"]
                if idx == 0 and "seed" in self.config
                else 0
            )
            maze = MazeGenerator(
                (lvl["width"], lvl["height"]),
                perfect=False,
                seed=lvl_seed,
            ).maze
            self.mazes.append(maze)

        first_maze = (
            self.mazes[0] if self.mazes else MazeGenerator((9, 11)).maze
        )
        self.update_dimensions(first_maze)

        # Initialize Game Engine
        self.engine = GameEngine(
            first_maze,
            self.cell_center,
            self.cell_size,
            theme=self.theme,
            game_config=config,
        )
        self.enter_text = arcade.Text(
            "Please enter your name for the highscore",
            cx,
            cy + 100,
            (80, 80, 80, 180),
            32,
            anchor_x="center",
            font_name="Renogare",
        )
        self.level_text = arcade.Text(
            f"LEVEL: {self.current_level_index + 1}",
            x=20,
            y=1040,
            color=arcade.color.YELLOW,
            font_name="Renogare",
            font_size=24,
        )
        self.sec = 0.0

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
        self.text = Text(self.center_x, self.center_y, config)

        self.pointer_text = arcade.Text(
            "|",
            self.text.text_name.right + 5,
            cy,
            (80, 80, 80, 180),
            32,
            anchor_x="center",
            font_name="Renogare",
        )
        self.on_remove = False
        self.on_remove_timer = 0.0

    @property
    def progress(self) -> float:
        return self.engine.progress

    def update_dimensions(self, maze: list[list[int]]) -> None:
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

    def next_level(self) -> None:
        if self.current_level_index + 1 >= len(self.levels):
            self.engine.pacman.final_score = self.engine.pacman.score
            self.engine.state = 3
            self.engine.pause = 1
            return
        saved_score = self.engine.pacman.score
        saved_deaths = self.engine.pacman.death_count

        self.current_level_index += 1
        self.level_text.text = f"LEVEL: {self.current_level_index + 1}"
        new_maze = self.mazes[self.current_level_index]
        self.update_dimensions(new_maze)

        self.engine = GameEngine(
            new_maze,
            self.cell_center,
            self.cell_size,
            theme=self.theme,
            game_config=self.config,
        )
        self.engine.pacman.score = saved_score
        self.engine.pacman.score_text.text = f"SCORE: {saved_score}"
        self.engine.pacman.death_count = saved_deaths

    def back_to_menu(self) -> None:
        self.window.show_view(self.screen_view)

    def on_text(self, text: str) -> None:
        if self.on_name:
            self.text.on_text(text)

    def toggle_theme(self, new_theme: str) -> None:
        self.theme = new_theme if new_theme in THEMES else "dark"
        self.theme_colors = THEMES.get(self.theme, THEMES["dark"])
        self.background_color = self.theme_colors["background"]
        self.pause_text.color = self.theme_colors["pause_text"]
        self.won_text.color = self.theme_colors["won_text"]
        self.engine.pacman.score_text.color = self.theme_colors["hud_text"]
        self.engine.pacman.lives_text.color = self.theme_colors["hud_text"]
        self.engine.time_text.color = self.theme_colors["hud_text"]
        self.level_text.color = self.theme_colors["hud_text"]
        ghost_colors = self.theme_colors["ghosts"]
        for i, ghost in enumerate(self.engine.ghosts):
            ghost.color = ghost_colors[i % len(ghost_colors)]
        for dot in self.engine.dots:
            if isinstance(dot, arcade.SpriteCircle):
                dot.color = self.theme_colors["dot"]

    def on_show_view(self) -> None:
        if self.music_player is None:
            self.music_player = self.audio_engine.music.play(
                self.volume, loop=True
            )
        elif not self.music_player.playing:
            self.music_player.play()

    def on_hide_view(self) -> None:
        if self.music_player and self.music_player.playing:
            self.music_player.pause()

    def cell_center(self, grid_x: float, grid_y: float) -> tuple[float, float]:
        sidebar_width = 170
        padding = 20
        cx = sidebar_width + (self.width - sidebar_width - padding) / 2
        cy = self.height / 2

        screen_x = cx + (grid_x - self.half_width) * self.cell_size
        screen_y = cy - (grid_y - self.half_height) * self.cell_size
        return (screen_x, screen_y)

    def reset_game(self) -> None:
        self.engine.reset_game()
        self.won_text.font_size = 280
        self.won_text.y = self.height / 2
        self.enter_text.y = self.height / 2 + 100
        self.text.cy = self.height / 2
        self.text.text_name.y = self.height / 2
        self.pointer_text.y = self.height / 2
        self.text.name = ""
        self.text.update_text()
        self.on_name = False

    def on_key_release(self, symbol: int, modifiers: int) -> None:
        if self.engine.state in (1, 3):
            if symbol == arcade.key.BACKSPACE:
                self.on_remove = False
                self.on_remove_timer = 0.0

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        if self.engine.state in (1, 3):
            if symbol == arcade.key.ENTER:
                score = (
                    self.engine.pacman.final_score
                    if self.engine.pacman.final_score
                    else self.engine.pacman.score
                )
                if self.text.on_finish(score):
                    self.on_name = False
                    self.back_to_menu()
            if symbol == arcade.key.BACKSPACE:
                if self.text.name:
                    self.on_remove = True
                    self.text.name = self.text.name[:-1]
                    self.text.update_text()
            if symbol == arcade.key.ESCAPE:
                self.on_name = False
                self.back_to_menu()
            return

        if symbol == arcade.key.C and modifiers & arcade.key.MOD_CTRL:
            sys.exit()
        if symbol == arcade.key.S and modifiers & arcade.key.MOD_CTRL:
            self.next_level()
        if symbol in (keys.get("UP", arcade.key.UP), arcade.key.W):
            self.engine.pacman.set_next_direction(Directions.UP)
        elif symbol in (keys.get("DOWN", arcade.key.DOWN), arcade.key.S):
            self.engine.pacman.set_next_direction(Directions.DOWN)
        elif symbol in (keys.get("RIGHT", arcade.key.RIGHT), arcade.key.D):
            self.engine.pacman.set_next_direction(Directions.RIGHT)
        elif symbol in (keys.get("LEFT", arcade.key.LEFT), arcade.key.A):
            self.engine.pacman.set_next_direction(Directions.LEFT)
        if symbol == arcade.key.ESCAPE:
            set_view = InGameSettings(self, self.screen_view)
            self.window.show_view(set_view)
        if symbol == arcade.key.SPACE:
            self.engine.state = 2
            self.engine.pause = not (self.engine.pause)

    def on_update(self, delta_time: float) -> None:
        if self.on_remove:
            self.on_remove_timer += delta_time
            if self.on_remove_timer > 0.4:
                self.text.name = self.text.name[:-1]
                self.text.update_text()
                self.on_remove_timer = 0.35
        self.engine.update(delta_time)
        if self.engine.level_cleared:
            self.engine.level_cleared = False
            self.next_level()
        self.pointer_text.x = self.text.text_name.right + 7
        if self.engine.state in (1, 3):
            score = self.engine.pacman.final_score
            self.enter_text.text = (
                f"score : {score}  Enter name for leaderboard"
            )
            self.enter_text.color = (
                arcade.color.RED
                if self.engine.state == 1
                else arcade.color.GREEN
            )
            if self.sec > 1.5:
                self.sec = 0.0
            self.sec += delta_time
        if self.engine.state == 3:
            t = self.engine.win_timer
            ease_out = t * (2 - t)
            self.won_text.font_size = int(280 - (280 - 60) * ease_out)
            self.won_text.y = self.height / 2 + 130 * ease_out
            self.enter_text.y = self.height / 2 + 40
            self.text.cy = self.height / 2 - 30
            self.text.text_name.y = self.height / 2 - 30
            self.pointer_text.y = self.height / 2 - 30

    def on_draw(self) -> None:
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
            real_x, real_y = self.cell_center(c, r)
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
        self.level_text.draw()
        self.engine.time_text.draw()

        max_lives = self.config.get("lives", 3)
        lives_remaining = max_lives - self.engine.pacman.death_count
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
            if self.engine.state in (1, 3):
                self.on_name = True
                name_rect = arcade.rect.XYWH(cx, cy, self.width, self.height)
                arcade.draw_rect_filled(name_rect, (10, 10, 10, 200))
                if self.engine.state == 3:
                    self.won_text.draw()
                self.enter_text.draw()
                self.text.text_name.draw()
                if self.sec < 0.75:
                    self.pointer_text.draw()

            if self.engine.state == 2:
                self.pause_text.draw()
