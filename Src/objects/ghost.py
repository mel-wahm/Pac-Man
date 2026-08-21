import math
import random

import arcade

from ..core import (
    DIR_DATA,
    Directions,
    construct_path,
    shortest_path,
)


class Ghost:
    def __init__(self, r_c, draw_cords, maze, color, c_size):
        self.r_c = r_c
        self.default = r_c
        self.smooth_x = float(r_c[0])
        self.smooth_y = float(r_c[1])
        self.ghost_freeze = 1
        self.draw_cords = draw_cords
        self.maze = maze
        self.color = color
        self.c_size = c_size
        self.path = []
        self.direction = Directions.LEFT
        self.next_direction = Directions.RIGHT
        self.edible_timer = 0
        self.sec = 0
        self.select = 0
        self.choices = [
            Directions.LEFT,
            Directions.RIGHT,
            Directions.UP,
            Directions.DOWN,
        ]
        self.opposites = {
            Directions.LEFT: Directions.RIGHT,
            Directions.RIGHT: Directions.LEFT,
            Directions.UP: Directions.DOWN,
            Directions.DOWN: Directions.UP,
        }
        self.edible = 0
        self.anim_time = 0.0
        self.eye_time = 0.0
        self.flash_speed = 0

    def reset_game(self):
        self.ghost_freeze = 2
        self.r_c = self.default
        self.smooth_x = float(self.default[0])
        self.smooth_y = float(self.default[1])
        self.path = []

    def can_turn(self, x, y, direction):
        mask, _, _, _ = DIR_DATA[direction]
        return not (self.maze[y][x] & mask)

    def get_direction(self, current, target):
        x, y = current
        nx, ny = target
        if nx == x + 1:
            return Directions.RIGHT
        if nx == x - 1:
            return Directions.LEFT
        if ny == y + 1:
            return Directions.UP
        if ny == y - 1:
            return Directions.DOWN

    def choose_target(self, pacman):
        x, y = self.r_c
        pac = (pacman.x, pacman.y)

        self.path = construct_path(
            pac, self.r_c, shortest_path(self.r_c, pac, self.maze)
        )
        close = len(self.path) > 1 and len(self.path) < max(
            len(self.maze[0]) / 2, len(self.maze) / 2
        )
        if close and not self.edible:
            self.r_c = self.path[1]
        else:
            valid_moves = []
            for d in self.choices:
                if d != self.opposites.get(self.direction):
                    mask, dx, dy, _ = DIR_DATA[d]
                    if not (self.maze[y][x] & mask):
                        valid_moves.append((x + dx, y + dy, d))
            if not valid_moves:
                self.direction = self.opposites[self.direction]
                self.next_direction = self.opposites[self.next_direction]
            else:
                if close and self.edible:
                    furthest = max(
                        valid_moves,
                        key=lambda move: math.hypot(
                            (move[0] - pacman.x), (move[1] - pacman.y)
                        ),
                    )
                    self.r_c = (furthest[0], furthest[1])
                    self.direction = furthest[2]
                else:
                    next_x, next_y, new_dir = random.choice(valid_moves)
                    self.r_c = (next_x, next_y)
                    self.direction = new_dir

        cols = len(self.maze[0])
        rows = len(self.maze)
        gx, gy = self.r_c

        if gx < 0:
            gx = cols - 1
            self.smooth_x = float(cols - 1)
        elif gx > cols - 1:
            gx = 0
            self.smooth_x = 0.0

        if gy < 0:
            gy = rows - 1
            self.smooth_y = float(rows - 1)
        elif gy > rows - 1:
            gy = 0
            self.smooth_y = 0.0

        self.r_c = (gx, gy)

    def update(self, speed, delta_time):
        self.smooth_x += (self.r_c[0] - self.smooth_x) * speed * delta_time
        self.smooth_y += (self.r_c[1] - self.smooth_y) * speed * delta_time
        self.anim_time += delta_time
        self.eye_time += delta_time * 8
        self.edible_timer = max(0, self.edible_timer - delta_time)
        if not self.edible_timer:
            self.edible = False
        self.sec += delta_time
        self.flash_speed = 0.3 if self.edible_timer > 1 else 0.15
        if self.sec > self.flash_speed:
            self.sec = 0
            self.select += 1

    def draw(self):
        white = arcade.color.WHITE
        cx, cy = self.draw_cords
        s = 0.002 * self.c_size

        if not self.edible:
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
                    eye_x,
                    cy + 15 * s,
                    30 * s,
                    white,
                    num_segments=32,
                )
                arcade.draw_circle_filled(
                    eye_x, cy + 15 * s, 20 * s, (33, 33, 255), num_segments=32
                )
                arcade.draw_circle_filled(
                    eye_x,
                    cy + 19 * s,
                    3 * s,
                    arcade.color.WHEAT,
                    num_segments=32,
                )
        else:
            if self.edible_timer < 4:
                edible_color = [(0, 0, 164), (255, 255, 255)][self.select % 2]
                pupil_color = [(255, 184, 82), (220, 20, 20)][self.select % 2]
                mouth_color = [white, (220, 20, 20)][self.select % 2]
            else:
                edible_color = (0, 0, 164)
                pupil_color = (255, 184, 82)
                mouth_color = white

            arcade.draw_arc_filled(
                cx, cy + 15 * s, 240 * s, 240 * s, edible_color, 0, 180
            )
            rect = arcade.rect.XYWH(cx, cy - 30 * s, 240 * s, 90 * s)
            arcade.draw_rect_filled(rect, edible_color)

            eye_x = math.cos(self.eye_time) * 3
            eye_y = math.sin(self.eye_time) * 3

            for ex in (cx - 35 * s, cx + 35 * s):
                arcade.draw_circle_filled(
                    ex,
                    cy + 40 * s,
                    30 * s,
                    white,
                    num_segments=32,
                )
                arcade.draw_circle_filled(
                    ex + eye_x * s * 2,
                    cy + 40 * s - eye_y * s * 2,
                    18 * s,
                    pupil_color,
                    num_segments=32,
                )

            mouth_x = cx - 80 * s
            mouth = []
            for i in range(20):
                xs = mouth_x + i * 8 * s
                y = cy - 40 * s + 16 * s * math.sin(i + self.anim_time * 5)
                mouth.append((xs, y))

            arcade.draw_line_strip(mouth, mouth_color, max(2, int(6 * s)))

            arcade.draw_arc_filled(
                cx, cy - 75 * s, 80 * s, 80 * s, edible_color, 180, 360
            )
            arcade.draw_arc_filled(
                cx - 80 * s,
                cy - 75 * s,
                80 * s,
                80 * s,
                edible_color,
                180,
                360,
            )
            arcade.draw_arc_filled(
                cx + 80 * s,
                cy - 75 * s,
                80 * s,
                80 * s,
                edible_color,
                180,
                360,
            )
