import arcade
from game import Game

class   Settings(arcade.View):
    def __init__(self, previous_view):
        super().__init__()
        self.settings_wallpaper = arcade.load_texture("photos/settings2.png")
        self.previous_view = previous_view
        self.cx, self.cy = self.width / 2, self.height / 2

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.Q:
            exit()
        if symbol == arcade.key.ESCAPE:
            self.window.show_view(self.previous_view)

    def on_draw(self):
        r = arcade.rect.XYWH(self.cx, self.cy, 1980, 1080)
        arcade.draw_texture_rect(self.settings_wallpaper, r)
