import arcade

from ..ui import Menu, Selection
from .key_bindings_view import Control


class Settings(arcade.View):
    def __init__(self, previous_view, game_view):
        super().__init__()
        self.wallpapers = {
            "dark": arcade.load_texture("photos/settings.png"),
            "light": arcade.load_texture("photos/light_settings.png"),
        }
        self.previous_view = previous_view
        self.game_view = game_view

        self.theme_option = Selection(f"Theme: {game_view.theme.capitalize()}", lambda: self.start_listening())
        self.return_option = Selection("Return", lambda: self.return_to_previous())
        self.controls_option = Selection("Controls", lambda: self.open_controls())
        self.menu = Menu(
            [self.controls_option,
             self.theme_option, self.return_option], self.width / 2, self.height / 2
        )

        self.press_key_text = arcade.Text(
            "Choose a theme",
            self.width / 2,
            self.height / 2 + 70,
            (180, 180, 180),
            40,
            anchor_x="center",
            font_name="Renogare",
        )
        self.dark_label = arcade.Text(
            "Dark",
            self.width / 2 - 120,
            self.height / 2 - 20,
            arcade.color.WHITE,
            40,
            anchor_x="center",
            font_name="Renogare",
        )
        self.light_label = arcade.Text(
            "Light",
            self.width / 2 + 120,
            self.height / 2 - 20,
            arcade.color.WHITE,
            40,
            anchor_x="center",
            font_name="Renogare",
        )
        self.theme_options = ["dark", "light"]
        self.theme_selected_index = 0 if game_view.theme == "dark" else 1
        self.theme_scale = 1.0
        self.is_listening = False

    def return_to_previous(self):
        self.window.show_view(self.previous_view)

    def start_listening(self):
        self.theme_selected_index = 0 if self.game_view.theme == "dark" else 1
        self.theme_scale = 1.0
        self.is_listening = True

    def open_controls(self):
        control_view = Control(self)
        self.window.show_view(control_view)

    def on_update(self, delta_time):
        if self.is_listening:
            if self.theme_scale < 2:
                self.theme_scale += delta_time * 3
        else:
            if self.menu.scale < 2:
                self.menu.scale += delta_time * 3

    def on_key_press(self, symbol, modifiers):
        if self.is_listening:
            if symbol == arcade.key.ESCAPE:
                self.is_listening = False
                return
            if symbol == arcade.key.LEFT:
                self.theme_selected_index = (self.theme_selected_index - 1) % 2
                self.theme_scale = 1.0
                return
            if symbol == arcade.key.RIGHT:
                self.theme_selected_index = (self.theme_selected_index + 1) % 2
                self.theme_scale = 1.0
                return
            if symbol == arcade.key.ENTER:
                new_theme = self.theme_options[self.theme_selected_index]
                self.game_view.toggle_theme(new_theme)
                self.theme_option.name = f"Theme: {new_theme.capitalize()}"
                self.menu.labels[1].text = f"Theme: {new_theme.capitalize()}"
                self.is_listening = False
                return
            return

        if symbol == arcade.key.UP:
            self.menu.move_up()
        if symbol == arcade.key.DOWN:
            self.menu.move_down()
        if symbol == arcade.key.ENTER:
            self.menu.action()
        if symbol == arcade.key.ESCAPE:
            self.window.show_view(self.previous_view)

    def on_mouse_motion(self, x, y, dx, dy):
        if not self.is_listening:
            self.menu.mouse_motion(x, y)
        else:
            dark_hit = (
                self.dark_label.left < x < self.dark_label.right
                and self.dark_label.bottom < y < self.dark_label.top
            )
            light_hit = (
                self.light_label.left < x < self.light_label.right
                and self.light_label.bottom < y < self.light_label.top
            )
            if dark_hit and self.theme_selected_index != 0:
                self.theme_selected_index = 0
                self.theme_scale = 1.0
            elif light_hit and self.theme_selected_index != 1:
                self.theme_selected_index = 1
                self.theme_scale = 1.0

    def on_mouse_press(self, x, y, button, modifiers):
        if not self.is_listening:
            self.menu.mouse_press(x, y)
        else:
            dark_hit = (
                self.dark_label.left < x < self.dark_label.right
                and self.dark_label.bottom < y < self.dark_label.top
            )
            light_hit = (
                self.light_label.left < x < self.light_label.right
                and self.light_label.bottom < y < self.light_label.top
            )
            if dark_hit or light_hit:
                new_theme = self.theme_options[self.theme_selected_index]
                self.game_view.toggle_theme(new_theme)
                self.theme_option.name = f"Theme: {new_theme.capitalize()}"
                self.menu.labels[1].text = f"Theme: {new_theme.capitalize()}"
                self.is_listening = False

    def on_draw(self):
        self.clear()
        screen_rect = arcade.rect.XYWH(
            self.width / 2, self.height / 2, self.window.width, self.window.height
        )
        if self.game_view.theme == "dark":
            wallpaper = self.wallpapers["dark"]
            menu_color = arcade.color.WHITE
            listen_overlay = (10, 16, 35, 230)
            prompt_color = (180, 180, 180)
            unselected_color = arcade.color.WHITE
        else:
            wallpaper = self.wallpapers["light"]
            menu_color = arcade.color.BLACK
            listen_overlay = (245, 248, 255, 230)
            prompt_color = (40, 50, 75)
            unselected_color = (40, 50, 75)

        arcade.draw_texture_rect(wallpaper, screen_rect)

        if not self.is_listening:
            self.menu.draw(menu_color)
        else:
            arcade.draw_rect_filled(screen_rect, listen_overlay)
            self.press_key_text.color = prompt_color
            self.press_key_text.draw()

            if self.theme_selected_index == 0:
                self.dark_label.color = arcade.color.YELLOW
                self.dark_label.font_size = int(40 * min(1.5, self.theme_scale))
                self.light_label.color = unselected_color
                self.light_label.font_size = 40
            else:
                self.light_label.color = arcade.color.YELLOW
                self.light_label.font_size = int(40 * min(1.5, self.theme_scale))
                self.dark_label.color = unselected_color
                self.dark_label.font_size = 40

            self.dark_label.draw()
            self.light_label.draw()
