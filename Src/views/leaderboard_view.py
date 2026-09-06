import arcade
import json

class Board(arcade.View):
    def __init__(self, previous_view):
        super().__init__()
        self.previous_view = previous_view
        arcade.load_font("fonts/Renogare-Regular.otf")
        self.cx = self.width / 2
        self.cy = self.height / 2
        self.background_color = (0, 0, 15)
        self.path = "Src/config/leaderboard.json"
        self.scroller = 0
        self.board = self.load_json()
        self.texts = self.board_texts()
        self.leaderboard_text1 = arcade.Text("Leaderboard",
                self.cx, self.height - 100,
                (231, 255, 244), 50, font_name="Renogare",
                anchor_x="center", anchor_y="center")
        self.leaderboard_text2 = arcade.Text("Leaderboard",
                self.cx - 2, self.height - 102,
                (50, 100, 244, 180), 50, font_name="Renogare",
                anchor_x="center", anchor_y="center")
        self.leaderboard_text3 = arcade.Text("Leaderboard",
                self.cx - 4, self.height - 104,
                (50, 100, 244, 120), 50, font_name="Renogare",
                anchor_x="center", anchor_y="center")
        self.background = arcade.load_texture("wallpaper/dark_wallpaper.png")
        self.pointer_text = arcade.Text(">", self.cx - 350, self.cy, arcade.color.YELLOW, 24, bold=True)

    def load_json(self):
        with open(self.path) as f:
            if not f.read().strip():
                return {}
            f.seek(0)
            board = json.load(f)
        return sorted(board, key=lambda x: x["score"], reverse=True)
    
    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.Q:
            self.window.close()
        if symbol == arcade.key.UP:
            self.scroller = max(0, self.scroller - 1)
            self.texts = self.board_texts()
        if symbol == arcade.key.DOWN:
            self.scroller = min(9, self.scroller + 1)
            self.texts = self.board_texts()
        if symbol == arcade.key.ESCAPE:
            self.window.show_view(self.previous_view)

    def board_texts(self):
        board = []
        gap = 50
        for idx, object in enumerate(self.board):
            print(idx)
            for g, (name, score) in enumerate(object.items()):
                k = 0.6
                d = idx - self.scroller
                alpha = 255 * (2.5 ** (-k * abs(d)))
                color = (255, 255, 255, int(alpha))
                if idx == self.scroller:
                    color = arcade.color.YELLOW

                y = self.cy - gap * idx + self.scroller * 50
                name_text = arcade.Text(
                    name,
                    self.cx - 300,
                    y,
                    color,
                    32,
                    anchor_x="left",
                    font_name="Renogare"
                )
                score_text = arcade.Text(
                    str(score),
                    self.cx + 300,
                    y,
                    color,
                    32,
                    anchor_x="right",
                    font_name="Renogare"
                )
                board.append((name_text, score_text))
        return board

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        if scroll_y > 0:
            self.scroller = max(0, self.scroller - 1)
            self.texts = self.board_texts()
        elif scroll_y < 0:
            self.scroller = min(9, self.scroller + 1)
            self.texts = self.board_texts()

    def on_update(self, delta_time):
        pass


    def on_draw(self):
        self.clear()
        r = arcade.rect.XYWH(self.cx, self.height - 100,
                            200, 45)
        arcade.draw_rect_filled(r, (240, 240, 240))
        r = arcade.rect.XYWH(self.cx, self.cy, self.width, self.height)
        arcade.draw_texture_rect(self.background, r)
        self.pointer_text.draw()
        self.leaderboard_text1.draw()
        self.leaderboard_text2.draw()
        self.leaderboard_text3.draw()
        for name, score in self.texts:
            name.draw()
            score.draw()
