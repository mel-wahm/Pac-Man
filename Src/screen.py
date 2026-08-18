import arcade

from mazegenerator import MazeGenerator

from . import config
from .credits import Credits
from .game import Game
from .menu import Menu, Selection
from .settings import Settings

class Screen(arcade.View):
    def __init__(self):
        super().__init__()
        self.wallpaper = arcade.load_texture("wallpaper/wallpaper.png")
        arcade.load_font("fonts/arcade_font.ttf")
        arcade.load_font("fonts/Renogare-Regular.otf")
        self.cx, self.cy = self.width / 2, self.height / 2
        self.start = Selection("Start", lambda: self.start_game())
        self.settings = Selection("Settings", lambda: self.enter_settings())
        self.credits = Selection("Credits", lambda: self.show_credits())
        self.exit = Selection("Exit", lambda: self.exit_game())
        self.menus = Menu(
            [self.start, self.settings, self.credits, self.exit],
            self.width / 2,
            self.height / 2,
        )
        maze = MazeGenerator(config.MAZE_SIZE).maze
        self.game_view = Game(maze, self)

    def start_game(self):
        maze = MazeGenerator(config.MAZE_SIZE).maze
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
        if self.menus.scale < 2:
            self.menus.scale += delta_time * 3

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.DOWN:
            self.menus.move_down()
        if symbol == arcade.key.UP:
            self.menus.move_up()
        if symbol == arcade.key.ENTER:
            self.menus.action()

    def on_mouse_motion(self, x, y, dx, dy):
        self.menus.mouse_motion(x, y, self.menus)
        
    def on_mouse_press(self, x, y, button, modifiers):
        self.menus.mouse_press(x, y, self.menus)

    def on_draw(self):
        self.clear()
        r = arcade.rect.XYWH(self.width / 2, self.height / 2, self.width, self.height)
        arcade.draw_texture_rect(self.wallpaper, r)
        self.menus.draw_texts()
