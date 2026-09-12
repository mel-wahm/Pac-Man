import arcade
from ..ui.menu import Menu, Selection
from ..config import config


class CheatMode(arcade.View):
    def __init__(self, game_engine, previous_view):
        super().__init__()
        self.game_engine = game_engine
        self.previous_view = previous_view
        self.inv = Selection("Invincibility", lambda: self.invincible())
        self.frz = Selection("Ghost Freeze", lambda: self.freeze())
        self.menus = Menu([self.inv, self.frz],
                    self.width / 2, self.height / 2)

    def invincible(self):
        config.pacman_inv = not config.pacman_inv

    def freeze(self):
        config.ghost_freeze = not config.ghost_freeze

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.UP:
            self.menus.move_up()
        if symbol == arcade.key.DOWN:
            self.menus.move_down()
        if symbol == arcade.key.ENTER:
            self.menus.action()
        if symbol == arcade.key.ESCAPE:
            self.window.show_view(self.previous_view)

    def on_update(self, delta_time: float) -> None:
        if config.pacman_inv:
            self.menus.labels[0].text = "- Invincibility"
        else:
            self.menus.labels[0].text = "Invincibility"

        if config.ghost_freeze:
            self.menus.labels[1].text = "- Ghost Freeze"
        else:
            self.menus.labels[1].text = "Ghost Freeze"

        if self.menus.scale < 1.3:
            self.menus.scale += delta_time * 3

    def on_draw(self):
        self.clear()
        x = self.width
        y = self.height
        self.previous_view.on_draw()
        r = arcade.rect.XYWH(x / 2, y / 2,
                             x, y)
        arcade.draw_rect_filled(r, (0, 0, 0, 245))
        self.menus.draw()
