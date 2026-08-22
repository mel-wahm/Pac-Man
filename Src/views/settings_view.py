import arcade

from ..ui import Menu, Selection
from .key_bindings_view import Control


class Settings(arcade.View):
    def __init__(self, previous_view, game_view):
        super().__init__()
        self.settings_wallpaper = arcade.load_texture("photos/settings.png")
        self.previous_view = previous_view
        self.game_view = game_view

        self.return_option = Selection("Return", lambda: self.return_to_previous())
        self.controls_option = Selection("Controls", lambda: self.open_controls())
        self.menu = Menu(
            [self.controls_option, self.return_option], self.width / 2, self.height / 2
        )

    def return_to_previous(self):
        self.window.show_view(self.previous_view)

    def open_controls(self):
        control_view = Control(self)
        self.window.show_view(control_view)

    def on_update(self, delta_time):
        self.menu.scale += delta_time * 3

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.UP:
            self.menu.move_up()
        if symbol == arcade.key.DOWN:
            self.menu.move_down()
        if symbol == arcade.key.ENTER:
            self.menu.action()
        if symbol == arcade.key.ESCAPE:
            self.window.show_view(self.previous_view)

    def on_mouse_motion(self, x, y, dx, dy):
        self.menu.mouse_motion(x, y)

    def on_mouse_press(self, x, y, button, modifiers):
        self.menu.mouse_press(x, y)

    def on_draw(self):
        self.clear()
        screen_rect = arcade.rect.XYWH(
            self.width / 2, self.height / 2, self.window.width, self.window.height
        )
        arcade.draw_texture_rect(self.settings_wallpaper, screen_rect)
        self.menu.draw_texts()
