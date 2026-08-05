import random
import arcade
from game_logic import neighbor_coordinates, shortest_path, construct_path


class Ghost:
    def __init__(self, r_c, draw_cords, maze, color, c_size):
        self.r_c = r_c
        self.default = r_c
        self.smooth_x = float(r_c[0])
        self.smooth_y = float(r_c[1])
        self.draw_cords = draw_cords
        self.maze = maze
        self.color = color
        self.c_size = c_size
        self.path = []

    def choose_target(self, pacman):
        if len(self.path) > 1 and len(self.path) < 10:
            self.r_c = self.path[1]
        else:
            x, y = self.r_c
            self.r_c = random.choice(neighbor_coordinates(x, y, self.maze))
        pac = (pacman.x, pacman.y)
        self.path = construct_path(
					pac, self.r_c, shortest_path(self.r_c, pac, self.maze)
				)
		

    def update(self, speed, delta_time):
        self.smooth_x += (self.r_c[0] - self.smooth_x) * speed * delta_time
        self.smooth_y += (self.r_c[1] - self.smooth_y) * speed * delta_time
        
    def draw(self):
        cx, cy = self.draw_cords
        s = 0.002 * self.c_size

        arcade.draw_arc_filled(
            cx, cy + 15 * s, 240 * s, 240 * s, self.color, 0, 180
        )
        rect = arcade.rect.XYWH(cx, cy - 30 * s, 240 * s, 90 * s)
        arcade.draw_rect_filled(rect, self.color)

        arcade.draw_arc_filled(
            cx, cy - 75 * s, 80 * s, 80 * s, self.color, 180, 360
        )
        arcade.draw_arc_filled(
            cx - 80 * s, cy - 75 * s, 80 * s, 80 * s, self.color, 180, 360
        )
        arcade.draw_arc_filled(
            cx + 80 * s, cy - 75 * s, 80 * s, 80 * s, self.color, 180, 360
        )

        for eye_x in (cx - 35 * s, cx + 35 * s):
            arcade.draw_circle_filled(
                eye_x, cy + 15 * s, 30 * s, arcade.color.WHITE, num_segments=32
            )
            arcade.draw_circle_filled(
                eye_x, cy + 15 * s, 20 * s, (33, 33, 255), num_segments=32
            )
            arcade.draw_circle_filled(
                eye_x, cy + 19 * s, 3 * s, arcade.color.WHEAT, num_segments=32
            )
