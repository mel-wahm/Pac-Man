import arcade

from ..ui import Menu, Selection, AudioControl, ThemeToggle
from .key_bindings_view import Control


class Settings(arcade.View):
    def __init__(self, previous_view, game_view):
        super().__init__()
        self.theme = 0 if game_view.theme == "dark" else 1
        self.wallpapers = [
            arcade.load_texture("photos/settings.png"),
            arcade.load_texture("photos/light_settings.png"),
        ]
        self.previous_view = previous_view
        self.game_view = game_view

        cx = self.width / 2
        cy = self.height / 2

        # Audio
        text_color = (
            arcade.color.WHITE if not self.theme else arcade.color.BLACK
        )
        self.audio_control = AudioControl(cx, cy, text_color)

        # Themes
        self.theme_toggle = ThemeToggle(cx, cy, game_view.theme)

        self.on_audio = False
        self.on_theme = False

        self.audio_option = Selection("Audio", lambda: self.open_audio())
        self.theme_option = Selection("Theme", lambda: self.open_theme())
        self.controls_option = Selection(
            "Key Binding", lambda: self.open_controls()
        )
        self.return_option = Selection(
            "Return", lambda: self.return_to_previous()
        )
        self.menu = Menu(
            [
                self.audio_option,
                self.theme_option,
                self.controls_option,
                self.return_option,
            ],
            cx,
            cy,
        )

    def open_audio(self):
        self.on_audio = True

    def open_theme(self):
        self.on_theme = True

    def return_to_previous(self):
        self.window.show_view(self.previous_view)

    def open_controls(self):
        control_view = Control(self)
        self.window.show_view(control_view)

    def on_update(self, delta_time):
        if self.menu.scale < 1.3:
            self.menu.scale += delta_time * 3

    def on_key_press(self, symbol, modifiers):
        if self.on_audio:
            if symbol == arcade.key.ESCAPE:
                self.on_audio = False
            if symbol == arcade.key.LEFT:
                self.audio_control.volume_down()
                self._apply_volume()
            if symbol == arcade.key.RIGHT:
                self.audio_control.volume_up()
                self._apply_volume()
            return

        if self.on_theme:
            if symbol == arcade.key.ESCAPE:
                self.on_theme = False
            if symbol == arcade.key.LEFT or symbol == arcade.key.RIGHT:
                self.theme_toggle.move(self.game_view.theme)
            if symbol == arcade.key.ENTER:
                new_theme = self.theme_toggle.get_theme()
                self.game_view.toggle_theme(new_theme)
                self.theme = 0 if new_theme == "dark" else 1
                text_color = (
                    arcade.color.WHITE
                    if new_theme == "dark"
                    else arcade.color.BLACK
                )
                self.audio_control.text_color = text_color
                self.audio_control._rebuild_label()
                self.theme_toggle._update_display(new_theme)
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
        if not self.on_audio and not self.on_theme:
            self.menu.mouse_motion(x, y)

    def on_mouse_press(self, x, y, button, modifiers):
        if not self.on_audio and not self.on_theme:
            self.menu.mouse_press(x, y)

    def _apply_volume(self):
        vol = self.audio_control.volume / 10
        if self.game_view.music_player:
            self.game_view.music_player.volume = vol

    def on_draw(self):
        self.clear()
        screen_rect = arcade.rect.XYWH(
            self.width / 2,
            self.height / 2,
            self.window.width,
            self.window.height,
        )
        arcade.draw_texture_rect(self.wallpapers[self.theme], screen_rect)
        color = [arcade.color.WHITE, arcade.color.BLACK][self.theme]
        sel_color = [arcade.color.YELLOW, arcade.color.RED][self.theme]

        if self.on_audio:
            self.audio_control.draw()
            return
        if self.on_theme:
            self.theme_toggle.draw()
            return

        self.menu.draw(color, sel_color)
