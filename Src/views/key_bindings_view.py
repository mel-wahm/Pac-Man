import arcade
import pyglet

from ..config import keys
from ..ui import Menu, Selection


class Control(arcade.View):
    def __init__(self, previous_view):
        super().__init__()
        self.previous_view = previous_view
        self.wallpaper = arcade.load_texture("photos/settings.png")

        key_symbol = pyglet.window.key.symbol_string
        self.left_option = Selection(
            f"Move left:   {key_symbol(keys['LEFT'])}", lambda: self.start_listening("LEFT")
        )
        self.right_option = Selection(
            f"Move right:   {key_symbol(keys['RIGHT'])}", lambda: self.start_listening("RIGHT")
        )
        self.up_option = Selection(
            f"Move up:   {key_symbol(keys['UP'])}", lambda: self.start_listening("UP")
        )
        self.down_option = Selection(
            f"Move down:   {key_symbol(keys['DOWN'])}", lambda: self.start_listening("DOWN")
        )
        self.menu = Menu(
            [self.up_option, self.down_option, self.right_option, self.left_option],
            self.width / 2,
            self.height / 2,
            gap=80,
        )
        self.press_key_text = arcade.Text(
            "Press a key",
            self.width / 2,
            self.height / 2 + 50,
            (180, 180, 180),
            40,
            anchor_x="center",
            font_name="Renogare",
        )
        self.error_key_text = arcade.Text(
            "Key not supported",
            self.width / 2,
            self.height / 2,
            (180, 180, 180),
            40,
            anchor_x="center",
            font_name="Renogare",
        )
        self.selected_action_text = arcade.Text(
            "",
            self.width / 2,
            self.height / 2 - 50,
            (180, 180, 180),
            60,
            anchor_x="center",
            font_name="Renogare",
        )
        self.is_listening = False
        self.current_action = ""
        self.error_timer = 0.0

    # Backward compatibility
    @property
    def menus(self):
        return self.menu

    def on_update(self, delta_time):
        if self.error_timer > 0:
            self.error_timer -= delta_time
        if self.menu.scale < 2:
            self.menu.scale += delta_time * 3

    def on_key_press(self, symbol, modifiers):
        if self.is_listening:
            if symbol == arcade.key.ESCAPE:
                self.is_listening = False
                return
            if 97 <= symbol <= 122 or 65361 <= symbol <= 65364:
                if symbol in keys.values() and symbol != keys[self.current_action]:
                    self.error_timer = 1.0
                    self.error_key_text.text = "Key Already Used"
                    return
                keys[self.current_action] = symbol
                self.is_listening = False
                key_name = pyglet.window.key.symbol_string(symbol)
                action_name = self.current_action.lower()
                menu_item = self.menu.labels[self.menu.selected_index]
                menu_item.text = f"Move {action_name}:   {key_name}"
            else:
                self.error_key_text.text = "Key Not Supported"
                self.error_timer = 1.0
            return

        if symbol == arcade.key.ESCAPE:
            self.window.show_view(self.previous_view)
            return
        if symbol == arcade.key.UP and not self.is_listening:
            self.menu.move_up()
        if symbol == arcade.key.DOWN and not self.is_listening:
            self.menu.move_down()
        if symbol == arcade.key.ENTER:
            if not self.is_listening:
                self.menu.action()

    def start_listening(self, action_key):
        self.selected_action_text.text = action_key
        self.current_action = action_key
        self.is_listening = not self.is_listening

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

        if not self.is_listening:
            arcade.draw_rect_filled(screen_rect, (0, 0, 0, 120))
            self.menu.draw_texts()
        else:
            arcade.draw_rect_filled(screen_rect, (0, 0, 0, 220))
            if self.error_timer > 0:
                self.error_key_text.draw()
            else:
                self.press_key_text.draw()
                self.selected_action_text.draw()
