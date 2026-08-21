import arcade

from mazegenerator import MazeGenerator

from ..config import MAZE_SIZE
from ..ui import Menu, Selection


class InGameSettings(arcade.View):
    def __init__(self, game_view, screen_view):
        super().__init__()
        self.settings_wallpaper = arcade.load_texture("photos/settings.png")
        arcade.load_font("fonts/Renogare-Regular.otf")

        self.game_view = game_view
        self.screen_view = screen_view

        self.resume_option = Selection("Resume", lambda: self.resume_game())
        self.retry_option = Selection("Retry", lambda: self.retry_game())
        self.options_option = Selection("Options", lambda: self.open_options())
        self.main_menu_option = Selection("Main menu", lambda: self.return_to_main_menu())

        self.menu = Menu(
            [self.resume_option, self.retry_option, self.options_option, self.main_menu_option],
            self.width / 2,
            self.height / 2,
        )

    # Backward compatibility
    @property
    def menus(self):
        return self.menu

    def resume_game(self):
        self.window.show_view(self.game_view)

    def retry_game(self):
        maze = MazeGenerator(MAZE_SIZE).maze
        from .game_view import Game

        game_view = Game(maze, self.screen_view)
        self.window.show_view(game_view)

    def open_options(self):
        from .settings_view import Settings

        set_view = Settings(self, self.game_view)
        self.window.show_view(set_view)

    def return_to_main_menu(self):
        self.window.show_view(self.screen_view)

    def on_update(self, delta_time):
        if self.menu.scale < 2:
            self.menu.scale += delta_time * 3

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.UP:
            self.menu.move_up()
        if symbol == arcade.key.DOWN:
            self.menu.move_down()
        if symbol == arcade.key.ESCAPE:
            self.window.show_view(self.game_view)
        if symbol == arcade.key.ENTER:
            self.menu.action()

    def on_mouse_motion(self, x, y, dx, dy):
        self.menu.mouse_motion(x, y)

    def on_mouse_press(self, x, y, button, modifiers):
        self.menu.mouse_press(x, y)

    def on_draw(self):
        self.clear()
        self.game_view.on_draw()
        dim_rect = arcade.rect.XYWH(
            self.width / 2, self.height / 2, self.width, self.height
        )
        arcade.draw_rect_filled(dim_rect, (0, 0, 0, 220))
        self.menu.draw_texts()
