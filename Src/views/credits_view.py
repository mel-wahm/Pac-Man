import arcade


class Credits(arcade.View):
    def __init__(self, prev_view):
        super().__init__()
        self.prev_view = prev_view
        arcade.load_font("fonts/Renogare-Regular.otf")
        self.credits = arcade.Text(
            "Credits: ",
            self.width / 2,
            self.height / 2 + 80,
            arcade.color.WHITE,
            42,
            anchor_x="center",
            font_name="Renogare",
        )
        self.mel_wahm = arcade.Text(
            "Mel-wahm",
            self.width / 2 - 160,
            self.height / 2,
            arcade.color.WHITE,
            42,
            anchor_x="center",
            font_name="Renogare",
        )
        self.tsellak = arcade.Text(
            "Tsellak",
            self.width / 2 + 160,
            self.height / 2,
            arcade.color.WHITE,
            42,
            anchor_x="center",
            font_name="Renogare",
        )

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ESCAPE:
            self.window.show_view(self.prev_view)

    def on_draw(self):
        self.clear()
        r = arcade.rect.XYWH(self.width / 2, self.height / 2,
                             self.width, self.height)
        self.prev_view.on_draw()
        arcade.draw_rect_filled(r, (0, 0, 0, 240))
        self.credits.draw()
        self.mel_wahm.draw()
        self.tsellak.draw()
