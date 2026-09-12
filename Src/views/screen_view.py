from typing import Any, Dict
import arcade

from ..ui import Menu, Selection
from .credits_view import Credits
from .game_view import Game
from .leaderboard_view import Board
from .settings_view import Settings


class Screen(arcade.View):
    def __init__(self, config: Dict[str, Any]) -> None:
        super().__init__()
        self.config = config
        self.wallpapers = {
            "dark": arcade.load_texture("wallpaper/dark_wallpaper.png"),
            "light": arcade.load_texture("wallpaper/light_wallpaper.png"),
        }
        arcade.load_font("fonts/arcade_font.ttf")
        arcade.load_font("fonts/Renogare-Regular.otf")

        center_x = self.width / 2
        center_y = self.height / 2

        self.start_option = Selection("Start", lambda: self.start_game())
        self.settings_option = Selection(
            "Settings", lambda: self.enter_settings()
        )
        self.leaderboard = Selection(
            "Leaderboard", lambda: self.show_leaderboard()
        )
        self.credits_option = Selection("Credits", lambda: self.show_credits())
        self.instructions_option = Selection("instructions", lambda: self.instructions())
        self.exit_option = Selection("Exit", lambda: self.exit_game())

        self.menu = Menu(
            [
                self.start_option,
                self.settings_option,
                self.instructions_option,
                self.leaderboard,
                self.credits_option,
                self.exit_option,
            ],
            center_x,
            center_y,
        )
        self.game_view = Game(self, self.config)

    def start_game(self) -> None:
        self.game_view = Game(self, self.config)
        self.window.show_view(self.game_view)

    def show_leaderboard(self) -> None:
        board = Board(self, self.game_view.theme, self.config)
        self.window.show_view(board)

    def instructions(self):
        pass

    def show_credits(self) -> None:
        self.window.show_view(Credits(self))

    def enter_settings(self) -> None:
        settings_view = Settings(self, self.game_view)
        self.window.show_view(settings_view)

    def exit_game(self) -> None:
        self.window.close()

    def on_update(self, delta_time: float) -> None:
        if self.menu.scale < 1.3:
            self.menu.scale += delta_time * 3

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        if symbol == arcade.key.DOWN:
            self.menu.move_down()
        if symbol == arcade.key.UP:
            self.menu.move_up()
        if symbol == arcade.key.ENTER:
            self.menu.action()

    def on_mouse_motion(
        self, x: float, y: float, dx: float, dy: float
    ) -> None:
        self.menu.mouse_motion(x, y)

    def on_mouse_press(
        self, x: float, y: float, button: int, modifiers: int
    ) -> None:
        self.menu.mouse_press(x, y)

    def on_draw(self) -> None:
        self.clear()
        screen_rect = arcade.rect.XYWH(
            self.width / 2, self.height / 2, self.width, self.height
        )
        wallpaper = self.wallpapers.get(
            self.game_view.theme, self.wallpapers["dark"]
        )
        arcade.draw_texture_rect(wallpaper, screen_rect)
        menu_color = (
            arcade.color.BLACK
            if self.game_view.theme == "light"
            else arcade.color.WHITE
        )
        sel_color = (
            arcade.color.RED
            if self.game_view.theme == "light"
            else arcade.color.YELLOW
        )

        self.menu.draw(menu_color, sel_color)
