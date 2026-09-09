import arcade

from mazegenerator import MazeGenerator

from ..config import MAZE_SIZE
from ..ui import Menu, Selection
from .credits_view import Credits
from .game_view import Game
from .settings_view import Settings
from .leaderboard_view import Board

if MAZE_SIZE[0] < 8 or MAZE_SIZE[1] < 8:
    print("Maze coordinates are too small!")
    exit(1)
if MAZE_SIZE[0] > 40 or MAZE_SIZE[1] > 40:
    print("Maze coordinates are too big!")
    exit(1)


class Screen(arcade.View):
    def __init__(self):
        super().__init__()
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
        self.exit_option = Selection("Exit", lambda: self.exit_game())

        self.menu = Menu(
            [
                self.start_option,
                self.settings_option,
                self.leaderboard,
                self.credits_option,
                self.exit_option,
            ],
            center_x,
            center_y,
        )

        maze = MazeGenerator(MAZE_SIZE).maze
        self.game_view = Game(maze, self)

    def start_game(self):
        maze = MazeGenerator(MAZE_SIZE).maze
        self.game_view = Game(maze, self)
        self.window.show_view(self.game_view)

    def show_leaderboard(self):
        board = Board(self, self.game_view.theme)
        self.window.show_view(board)

    def show_credits(self):
        self.window.show_view(Credits(self))

    def enter_settings(self):
        settings_view = Settings(self, self.game_view)
        self.window.show_view(settings_view)

    def exit_game(self):
        self.window.close()

    def on_update(self, delta_time):
        if self.menu.scale < 1.3:
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
