import arcade

from mazegenerator import MazeGenerator

from ..config import MAZE_SIZE
from ..ui import Menu, Selection
from .credits_view import Credits
from .game_view import Game
from .settings_view import Settings


class Screen(arcade.View):
    def __init__(self):
        super().__init__()
        self.wallpaper = arcade.load_texture("wallpaper/wallpaper.png")
        arcade.load_font("fonts/arcade_font.ttf")
        arcade.load_font("fonts/Renogare-Regular.otf")

        center_x = self.width / 2
        center_y = self.height / 2

        self.start_option = Selection("Start", lambda: self.start_game())
        self.settings_option = Selection("Settings", lambda: self.enter_settings())
        self.credits_option = Selection("Credits", lambda: self.show_credits())
        self.exit_option = Selection("Exit", lambda: self.exit_game())

        self.menu = Menu(
            [self.start_option, self.settings_option, self.credits_option, self.exit_option],
            center_x,
            center_y,
        )

        maze = MazeGenerator(MAZE_SIZE).maze
        self.game_view = Game(maze, self)

    # Backward compatibility alias
    @property
    def menus(self):
        return self.menu

    def start_game(self):
        maze = MazeGenerator(MAZE_SIZE).maze
        self.game_view = Game(maze, self)
        self.window.show_view(self.game_view)

    def show_credits(self):
        self.window.show_view(Credits(self))

    def enter_settings(self):
        settings_view = Settings(self, self.game_view)
        self.window.show_view(settings_view)

    def exit_game(self):
        exit()

    def on_update(self, delta_time):
        if self.menu.scale < 2:
            self.menu.scale += delta_time * 3

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.DOWN:
            self.menu.move_down()
        if symbol == arcade.key.UP:
            self.menu.move_up()
        if symbol == arcade.key.ENTER:
            self.menu.action()

    def on_mouse_motion(self, x, y, dx, dy):
        self.menu.mouse_motion(x, y)

    def on_mouse_press(self, x, y, button, modifiers):
        self.menu.mouse_press(x, y)

    def on_draw(self):
        self.clear()
        screen_rect = arcade.rect.XYWH(
            self.width / 2, self.height / 2, self.width, self.height
        )
        arcade.draw_texture_rect(self.wallpaper, screen_rect)
        self.menu.draw_texts()
