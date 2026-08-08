import arcade
from game import Game
from mazegenerator import MazeGenerator
class   Screen(arcade.View):
    def __init__(self):
        super().__init__()
        self.wallpaper = arcade.load_texture("wallpaper/wallpaper2.png")
        arcade.load_font("fonts/arcade_font.ttf")
        self.cx, self.cy = self.width / 2, self.height / 2
        self.start_text = self.text_object("START", (self.cx - 100, self.cy + 80))
        self.settings_text = self.text_object("SETTINGS", (self.cx - 100, self.cy))
        self.exit_text = self.text_object("EXIT", (self.cx - 100, self.cy - 80))
        self.choice = 0
        self.choices = {
                        0: "START",
                        1: "SETTINGS",
                        2: "EXIT"
                    }

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.Q:
            exit()
        if symbol == arcade.key.DOWN:
            self.choice = min(2, self.choice + 1)
        if symbol == arcade.key.UP:
            self.choice = max(0, self.choice - 1)
        if symbol == arcade.key.ENTER:
            if not self.choice:
                maze = MazeGenerator((15, 15)).maze
                game_view = Game(maze)
                self.window.show_view(game_view)
            if self.choice == 2:
                exit()

    def text_object(self, text, pos):
        return arcade.Text(text, pos[0], pos[1], arcade.color.BLACK,
                           32, 11, anchor_y="center", font_name="Public Pixel")
        


    def on_draw(self):
        self.clear()
        r = arcade.rect.XYWH(self.cx, self.cy, 1980, 1080)
        arcade.draw_texture_rect(
            self.wallpaper,
            r
        )
        self.start_text.draw()
        self.settings_text.draw()
        self.exit_text.draw()
        arcade.draw_arc_filled(self.cx - 140,
                               self.cy + 78 -self.choice * 80,
                               40, 40 , arcade.color.SCHOOL_BUS_YELLOW, 30, 330)
