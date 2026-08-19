import arcade
import pyglet

from ..config import keys
from ..ui import Menu, Selection


class Control(arcade.View):
    def __init__(self, previous_view):
        super().__init__()
        self.previous_view = previous_view
        self.wallpaper = arcade.load_texture("photos/settings.png")
        k = keys
        ks = pyglet.window.key.symbol_string
        self.left = Selection(
            f"Move left:   {ks(k['LEFT'])}", lambda: self.listen("LEFT")
        )
        self.right = Selection(
            f"Move right:   {ks(k['RIGHT'])}", lambda: self.listen("RIGHT")
        )
        self.up = Selection(f"Move up:   {ks(k['UP'])}",
                            lambda: self.listen("UP"))
        self.down = Selection(
            f"Move down:   {ks(k['DOWN'])}", lambda: self.listen("DOWN")
        )
        self.menus = Menu(
            [self.up, self.down, self.right, self.left],
            self.width / 2,
            self.height / 2,
            gap=80,
        )
        self.press_key = arcade.Text(
            "Press a key",
            self.width / 2,
            self.height / 2 + 50,
            (180, 180, 180),
            40,
            anchor_x="center",
            font_name="Renogare",
        )
        self.error_key = arcade.Text(
            "Key not supported",
            self.width / 2,
            self.height / 2,
            (180, 180, 180),
            40,
            anchor_x="center",
            font_name="Renogare",
        )
        self.select_key = arcade.Text(
            "",
            self.width / 2,
            self.height / 2 - 50,
            (180, 180, 180),
            60,
            anchor_x="center",
            font_name="Renogare",
        )
        self.listening = 0
        self.current_action = ""
        self.timer = 0

    def on_update(self, delta_time):
        if self.timer > 0:
            self.timer -= delta_time
        if self.menus.scale < 2:
            self.menus.scale += delta_time * 3

    def on_key_press(self, symbol, modifiers):
        if self.listening:
            if symbol == arcade.key.ESCAPE:
                self.listening = False
                return
            if 97 <= symbol <= 122 or 65361 <= symbol <= 65364:
                if symbol in keys.values()\
                 and symbol != keys[self.current_action]:
                    self.timer = 1.0
                    self.error_key.text = "Key Already Used"
                    return
                keys[self.current_action] = symbol
                self.listening = 0
                key_name = pyglet.window.key.symbol_string(symbol)
                act_name = self.current_action.lower()
                item = self.menus.texts[self.menus.select]
                item.text = f"Move {act_name}:   {key_name}"
            else:
                self.error_key.text = "Key Not Supported"
                self.timer = 1.0
            return
        if symbol == arcade.key.ESCAPE:
            self.window.show_view(self.previous_view)
            return
        if symbol == arcade.key.UP and not self.listening:
            self.menus.move_up()
        if symbol == arcade.key.DOWN and not self.listening:
            self.menus.move_down()
        if symbol == arcade.key.ENTER:
            if not self.listening:
                self.menus.action()

    def listen(self, key):
        self.select_key.text = key
        self.current_action = key
        self.listening = not (self.listening)

    def on_mouse_motion(self, x, y, dx, dy):
        self.menus.mouse_motion(x, y, self.menus)

    def on_mouse_press(self, x, y, button, modifiers):
        self.menus.mouse_press(x, y, self.menus)

    def on_draw(self):
        self.clear()
        if not self.listening:
            r = arcade.rect.XYWH(
                self.width / 2, self.height / 2, self.width, self.height
            )
            arcade.draw_texture_rect(self.wallpaper, r)
            arcade.draw_rect_filled(r, (0, 0, 0, 120))
            self.menus.draw_texts()
        else:
            r = arcade.rect.XYWH(
                self.width / 2, self.height / 2, self.width, self.height
            )
            arcade.draw_texture_rect(self.wallpaper, r)
            r = arcade.rect.XYWH(
                self.width / 2, self.height / 2, self.width, self.height
            )
            arcade.draw_rect_filled(r, (0, 0, 0, 220))
            if self.timer > 0:
                self.error_key.draw()
            else:
                self.press_key.draw()
                self.select_key.draw()
