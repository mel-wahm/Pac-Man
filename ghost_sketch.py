import math
import arcade


class Sketch(arcade.Window):
    def __init__(self):
        super().__init__(1980, 1080, "SKETCH", True)
        self.anim_time = 0.0
        self.eye_time = 0.0
        self.pause = 0

    def on_update(self, delta_time):
        if not self.pause:
            self.anim_time += delta_time
            self.eye_time += delta_time * 8

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.Q:
            exit()
        if symbol == arcade.key.SPACE:
            self.pause = not (self.pause)

    def on_draw(self):
        cx, cy = self.width / 2, self.height / 2
        arcade.draw_arc_filled(cx - 100, cy + 100, 350, 350, (0, 0, 64), 0, 180)
        rec = arcade.rect.XYWH(cx - 100, cy + 33, 350, 150)
        arcade.draw_rect_filled(rec, (0, 0, 64))

        eye_x = math.cos(self.eye_time) * 3
        eye_y = math.sin(self.eye_time) * 3
        arcade.draw_arc_filled(cx - 150, cy + 140, 65, 90, arcade.color.WHITE, 0, 360)
        arcade.draw_arc_filled(
            cx - 150 + 5 * eye_x, cy + 140 - 5 * eye_y, 45, 60, (0, 0, 64), 0, 360
        )
        arcade.draw_arc_filled(cx - 60, cy + 140, 65, 90, arcade.color.WHITE, 0, 360)
        arcade.draw_arc_filled(
            cx - 60 + 5 * eye_x, cy + 140 - 5 * eye_y, 45, 60, (0, 0, 64), 0, 360
        )

        arcade.draw_arc_filled(cx + 15, cy - 40, 120, 100, (0, 0, 64), 180, 360)
        arcade.draw_arc_filled(cx - 100, cy - 40, 120, 100, (0, 0, 64), 180, 360)
        arcade.draw_arc_filled(cx - 215, cy - 40, 120, 100, (0, 0, 64), 180, 360)

        mlx = cx - 220
        mouth = []
        for i in range(20):
            xs = mlx + i * 12
            y = cy + 30 + 15 * math.sin(i + self.anim_time * 5)
            mouth.append((xs, y))

        arcade.draw_line_strip(mouth, arcade.color.WHITE, 12)


Sketch()
arcade.run()
