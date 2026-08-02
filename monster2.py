import arcade


class MonsterDemo(arcade.Window):
    def __init__(self):
        super().__init__(800, 600, 'Ghost Character', resizable=True)
        self.background_color = (15, 15, 25)

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.Q:
            exit(0)

    def draw_ghost(self, cx, cy, radius, color):
        """Draw a classic Pac-Man ghost."""
        # 1. Top head (semicircle from 0 to 180 degrees)
        arcade.draw_arc_filled(
            cx, cy, radius * 2, radius * 2,
            color, 0, 180
        )

        # 2. Body rectangle below the semicircle
        rect = arcade.rect.LBWH(cx - radius, cy - radius, radius * 2, radius)
        arcade.draw_rect_filled(rect, color)

        # 3. Wavy bottom (3 inverted semicircles)
        bumps = 3
        bump_w = (radius * 2) / bumps
        for i in range(bumps):
            bx = cx - radius + bump_w * i + bump_w / 2
            by = cy - radius
            arcade.draw_arc_filled(
                bx, by, bump_w, bump_w,
                color, 180, 360
            )

        # 4. Eyes (white sclera + dark pupil)
        eye_offset = radius * 0.3
        eye_r = radius * 0.22
        for ex in [cx - eye_offset, cx + eye_offset]:
            ey = cy + radius * 0.15
            arcade.draw_circle_filled(ex, ey, eye_r, arcade.color.WHITE)
            arcade.draw_circle_filled(
                ex + eye_r * 0.3, ey - eye_r * 0.1,
                eye_r * 0.5, (20, 20, 60)
            )

    def on_draw(self):
        self.clear()
        cx = self.width / 2
        cy = self.height / 2
        radius = min(self.width, self.height) * 0.2
        self.draw_ghost(cx, cy, radius, arcade.color.RED)


MonsterDemo()
arcade.run()
