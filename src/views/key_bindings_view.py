from typing import Any
import arcade
import pyglet

from ..config import keys
from ..ui import Menu, Selection
import json


class Control(arcade.View):
    def __init__(self, previous_view: Any) -> None:
        super().__init__()
        self.previous_view = previous_view
        self.wallpapers = {
            "dark": arcade.load_texture("photos/settings.png"),
            "light": arcade.load_texture("photos/light_settings.png"),
        }

        key_symbol = pyglet.window.key.symbol_string
        self.left_option = Selection(
            f"Move left:   {key_symbol(keys['LEFT'])}",
            lambda: self.start_listening("LEFT"),
        )
        self.right_option = Selection(
            f"Move right:   {key_symbol(keys['RIGHT'])}",
            lambda: self.start_listening("RIGHT"),
        )
        self.up_option = Selection(
            f"Move up:   {key_symbol(keys['UP'])}",
            lambda: self.start_listening("UP"),
        )
        self.down_option = Selection(
            f"Move down:   {key_symbol(keys['DOWN'])}",
            lambda: self.start_listening("DOWN"),
        )
        self.menu = Menu(
            [
                self.up_option,
                self.down_option,
                self.right_option,
                self.left_option,
            ],
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

    def on_update(self, delta_time: float) -> None:
        if self.error_timer > 0:
            self.error_timer -= delta_time
        if self.menu.scale < 1.3:
            self.menu.scale += delta_time * 3

    def update_json(self, json_file: str, key: str, value: str) -> None:
        with open(json_file) as f:
            js = f.read()
        js = json.loads(js)
        js[key] = value
        with open(json_file, "w") as f:
            f.write(json.dumps(js, indent=4))

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        if self.is_listening:
            if symbol == arcade.key.ESCAPE:
                self.is_listening = False
                return
            if 97 <= symbol <= 122 or 65361 <= symbol <= 65364:
                used_keys = set(keys.values()) | {
                    arcade.key.W,
                    arcade.key.A,
                    arcade.key.S,
                    arcade.key.D,
                }
                if (
                    symbol in used_keys
                    and symbol != keys[self.current_action]
                ):
                    self.error_timer = 1.0
                    self.error_key_text.text = "Key Already Used"
                    return
                keys[self.current_action] = symbol
                self.is_listening = False
                key_name = pyglet.window.key.symbol_string(symbol)
                self.update_json(
                    "src/config/keys.json",
                    self.current_action,
                    "arcade.key." + key_name,
                )
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

    def start_listening(self, action_key: str) -> None:
        self.selected_action_text.text = action_key
        self.current_action = action_key
        self.is_listening = not self.is_listening

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
        if self.previous_view.game_view.theme == "light":
            wallpaper = self.wallpapers["light"]
            menu_color = arcade.color.BLACK
            sel_color = arcade.color.RED
            listen_overlay = (245, 248, 255, 230)
            text_color = (40, 50, 75)
        else:
            wallpaper = self.wallpapers["dark"]
            menu_color = arcade.color.WHITE
            sel_color = arcade.color.YELLOW
            listen_overlay = (10, 16, 35, 230)
            text_color = (180, 180, 180)

        arcade.draw_texture_rect(wallpaper, screen_rect)

        if not self.is_listening:
            self.menu.draw(menu_color, sel_color)
        else:
            arcade.draw_rect_filled(screen_rect, listen_overlay)
            self.press_key_text.color = text_color
            self.selected_action_text.color = text_color
            if self.error_timer > 0:
                self.error_key_text.draw()
            else:
                self.press_key_text.draw()
                self.selected_action_text.draw()
