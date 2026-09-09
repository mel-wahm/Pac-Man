import arcade
import json


class Board(arcade.View):
    def __init__(self, previous_view, theme):
        super().__init__()
        self.previous_view = previous_view
        arcade.load_font("fonts/Renogare-Regular.otf")
        self.cx = self.width / 2
        self.cy = self.height / 2
        self.background_color = (0, 0, 15)
        self.path = "Src/config/leaderboard.json"
        self.scroller = 0
        self.theme = theme
        self.board = self.load_json()
        self.texts = self.board_texts()
        self.leaderboard_text1 = arcade.Text(
            "Leaderboard",
            self.cx,
            self.height - 100,
            (231, 255, 244),
            50,
            font_name="Renogare",
            anchor_x="center",
            anchor_y="center",
        )
        self.leaderboard_text2 = arcade.Text(
            "Leaderboard",
            self.cx - 2,
            self.height - 102,
            (50, 100, 244, 180),
            50,
            font_name="Renogare",
            anchor_x="center",
            anchor_y="center",
        )
        self.leaderboard_text3 = arcade.Text(
            "Leaderboard",
            self.cx - 4,
            self.height - 104,
            (50, 100, 244, 120),
            50,
            font_name="Renogare",
            anchor_x="center",
            anchor_y="center",
        )
        self.backgrounds = [arcade.load_texture("wallpaper/dark_wallpaper.png"),
                            arcade.load_texture("wallpaper/light_wallpaper.png")]
        self.background = self.backgrounds[0] if theme == "dark" else self.backgrounds[1]
        self.pointer_text = arcade.Text(
            ">", self.cx - 350, self.cy, arcade.color.YELLOW if theme == "dark" else arcade.color.RED
            , 24, bold=True
        )
        self.empty_board = arcade.Text(
            "The leaderboard is empty",
            self.cx,
            self.cy,
            (220, 220, 200, 120) if theme == "dark" else (10, 10, 10, 150),
            30,
            font_name="Renogare",
            anchor_x="center",
        )
        self.scrolling_up = False
        self.scrolling_down = False
        self.scrolling_timer = 0

    def load_json(self):
        with open(self.path) as f:
            if not f.read().strip():
                return []
            f.seek(0)
            board = json.load(f)
        return sorted(board, key=lambda x: x["score"], reverse=True)

    @staticmethod
    def update_json(path, name, score):
        new_score = {"name": name, "score": score}
        with open(path) as f:
            if not f.read().strip():
                board = []
            else:
                f.seek(0)
                board = json.load(f)
        board.append(new_score)
        with open(path, "w") as f:
            json.dump(board, f, indent=4)

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.UP:
            self.scroller = (self.scroller - 1) % len(self.board)
            self.texts = self.board_texts()
            self.scrolling_up = True
        if symbol == arcade.key.DOWN:
            self.scrolling_down = True
            self.scroller = (self.scroller + 1) % len(self.board)
            self.texts = self.board_texts()
        if symbol == arcade.key.ESCAPE:
            self.window.show_view(self.previous_view)

    def on_key_release(self, symbol: int, modifiers: int) -> bool | None:
        if symbol == arcade.key.UP:
            self.scrolling_timer = 0
            self.scrolling_up = False
        if symbol == arcade.key.DOWN:
            self.scrolling_timer = 0
            self.scrolling_down = False

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        if scroll_y > 0:
            self.scroller = (self.scroller - 1) % len(self.board)
            self.texts = self.board_texts()
        elif scroll_y < 0:
            self.scroller = (self.scroller + 1) % len(self.board)
            self.texts = self.board_texts()

    def board_texts(self):
        board = []
        gap = 50
        for idx, object in enumerate(self.board):
            name = object["name"]
            score = object["score"]
            k = 0.6
            d = idx - self.scroller
            alpha = 255 * (2.5 ** (-k * abs(d)))
            color = (255, 255, 255, int(alpha)) if self.theme == "dark" else (0, 0, 0, int(alpha))
                
            if idx == self.scroller:
                color = arcade.color.YELLOW if self.theme == "dark" else arcade.color.RED

            y = self.cy - gap * idx + self.scroller * 50
            name_text = arcade.Text(
                name,
                self.cx - 300,
                y,
                color,
                32,
                anchor_x="left",
                font_name="Renogare",
            )
            score_text = arcade.Text(
                str(score),
                self.cx + 300,
                y,
                color,
                32,
                anchor_x="right",
                font_name="Renogare",
            )
            board.append((name_text, score_text))
        return board

    def on_update(self, delta_time):
        if self.scrolling_down and self.scrolling_timer > 0.2:
            self.scroller = (self.scroller + 1) % len(self.board)
            self.texts = self.board_texts()

        if self.scrolling_up and self.scrolling_timer > 0.2:
            self.scroller = (self.scroller - 1) % len(self.board)
            self.texts = self.board_texts()

        if self.scrolling_timer > 0.2:
            self.scrolling_timer = 0
        if self.scrolling_down or self.scrolling_up:
            self.scrolling_timer += delta_time

    def on_draw(self):
        self.clear()
        r = arcade.rect.XYWH(self.cx, self.cy, self.width, self.height)
        arcade.draw_texture_rect(self.background, r)
        if self.texts:
            self.leaderboard_text1.draw()
            self.leaderboard_text2.draw()
            self.leaderboard_text3.draw()
            self.pointer_text.draw()
            for name, score in self.texts:
                name.draw()
                score.draw()
        else:
            self.empty_board.draw()
