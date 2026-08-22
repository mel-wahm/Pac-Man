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
    def __init__(self, grid_pos, draw_coords, maze, color, cell_size):
        self.grid_pos = grid_pos
        self.spawn_pos = grid_pos
        self.smooth_x = float(grid_pos[0])
        self.smooth_y = float(grid_pos[1])
        self.ghost_freeze = 1
        self.draw_coords = draw_coords
        self.maze = maze
        self.color = color
        self.cell_size = cell_size
        self.path = []
        self.direction = Directions.LEFT
        self.next_direction = Directions.RIGHT
        self.edible_timer = 0.0
        self.flash_timer = 0.0
        self.flash_index = 0
        self.flash_speed = 0.3
        self.eaten_timer = 0
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
        self.edible = False
        self.anim_time = 0.0
        self.eye_time = 0.0

    def reset_game(self):
        self.ghost_freeze = 2
        self.eaten_timer = 0
        self.grid_pos = self.spawn_pos
        self.smooth_x = float(self.spawn_pos[0])
        self.smooth_y = float(self.spawn_pos[1])
        self.path = []
        self.edible = False
        self.edible_timer = 0.0
        self.flash_timer = 0.0
        self.flash_index = 0

    def can_turn(self, x, y, direction):
        mask, _, _, _ = DIR_DATA[direction]
        return not (self.maze[y][x] & mask)

    def choose_target(self, pacman):
        x, y = self.grid_pos
        pac_pos = (pacman.x, pacman.y)

        self.path = construct_path(
            pac_pos, self.grid_pos, shortest_path(self.grid_pos, pac_pos, self.maze)
        )
        is_close = len(self.path) > 1 and len(self.path) < max(
            len(self.maze[0]) / 2, len(self.maze) / 2
        )

        if is_close and not self.edible:
            self.grid_pos = self.path[1]
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
                if is_close and self.edible:
                    furthest = max(
                        valid_moves,
                        key=lambda move: math.hypot(
                            (move[0] - pacman.x), (move[1] - pacman.y)
                        ),
                    )
                    self.grid_pos = (furthest[0], furthest[1])
                    self.direction = furthest[2]
                else:
                    next_x, next_y, new_dir = random.choice(valid_moves)
                    self.grid_pos = (next_x, next_y)
                    self.direction = new_dir

        cols = len(self.maze[0])
        rows = len(self.maze)
        gx, gy = self.grid_pos

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

        self.grid_pos = (gx, gy)

    def update(self, speed, delta_time):
        self.smooth_x += (self.grid_pos[0] - self.smooth_x) * speed * delta_time
        self.smooth_y += (self.grid_pos[1] - self.smooth_y) * speed * delta_time
        self.anim_time += delta_time
        self.eye_time += delta_time * 8.0
        self.edible_timer = max(0.0, self.edible_timer - delta_time)
        

        if not self.edible_timer:
            self.edible = False

        self.flash_timer += delta_time
        self.flash_speed = 0.3 if self.edible_timer > 1.0 else 0.20
        if self.flash_timer > self.flash_speed:
            self.flash_timer = 0.0
            self.flash_index += 1

    def draw(self):
        white = arcade.color.WHITE
        cx, cy = self.draw_coords
        scale = 0.002 * self.cell_size

        if not self.edible:
            # Body Dome & Rect
            arcade.draw_arc_filled(
                cx, cy + 15 * scale, 240 * scale, 240 * scale, self.color, 0, 180
            )
            rect = arcade.rect.XYWH(cx, cy - 30 * scale, 240 * scale, 90 * scale)
            arcade.draw_rect_filled(rect, self.color)

            # Skirt Tentacles
            arcade.draw_arc_filled(
                cx, cy - 75 * scale, 80 * scale, 80 * scale, self.color, 180, 360
            )
            arcade.draw_arc_filled(
                cx - 80 * scale, cy - 75 * scale, 80 * scale, 80 * scale, self.color, 180, 360
            )
            arcade.draw_arc_filled(
                cx + 80 * scale, cy - 75 * scale, 80 * scale, 80 * scale, self.color, 180, 360
            )

            # Eyes
            for eye_x in (cx - 35 * scale, cx + 35 * scale):
                arcade.draw_circle_filled(
                    eye_x,
                    cy + 15 * scale,
                    30 * scale,
                    white,
                    num_segments=32,
                )
                arcade.draw_circle_filled(
                    eye_x, cy + 15 * scale, 20 * scale, (33, 33, 255), num_segments=32
                )
                arcade.draw_circle_filled(
                    eye_x,
                    cy + 19 * scale,
                    3 * scale,
                    arcade.color.WHEAT,
                    num_segments=32,
                )
        else:
            if self.edible_timer < 4.0:
                is_flashing_white = (self.flash_index % 2 == 1)
                edible_color = (255, 255, 255) if is_flashing_white else (0, 0, 164)
                pupil_color = (220, 20, 20) if is_flashing_white else (255, 184, 82)
                mouth_color = (220, 20, 20) if is_flashing_white else white
            else:
                edible_color = (0, 0, 164)
                pupil_color = (255, 184, 82)
                mouth_color = white

            arcade.draw_arc_filled(
                cx, cy + 15 * scale, 240 * scale, 240 * scale, edible_color, 0, 180
            )
            rect = arcade.rect.XYWH(cx, cy - 30 * scale, 240 * scale, 90 * scale)
            arcade.draw_rect_filled(rect, edible_color)

            eye_x = math.cos(self.eye_time) * 3
            eye_y = math.sin(self.eye_time) * 3

            for ex in (cx - 35 * scale, cx + 35 * scale):
                arcade.draw_circle_filled(
                    ex,
                    cy + 40 * scale,
                    30 * scale,
                    white,
                    num_segments=32,
                )
                arcade.draw_circle_filled(
                    ex + eye_x * scale * 2,
                    cy + 40 * scale - eye_y * scale * 2,
                    18 * scale,
                    pupil_color,
                    num_segments=32,
                )

            mouth_x = cx - 80 * scale
            mouth = []
            for i in range(20):
                xs = mouth_x + i * 8 * scale
                y = cy - 40 * scale + 16 * scale * math.sin(i + self.anim_time * 5)
                mouth.append((xs, y))

            arcade.draw_line_strip(mouth, mouth_color, max(2, int(6 * scale)))

            arcade.draw_arc_filled(
                cx, cy - 75 * scale, 80 * scale, 80 * scale, edible_color, 180, 360
            )
            arcade.draw_arc_filled(
                cx - 80 * scale,
                cy - 75 * scale,
                80 * scale,
                80 * scale,
                edible_color,
                180,
                360,
            )
            arcade.draw_arc_filled(
                cx + 80 * scale,
                cy - 75 * scale,
                80 * scale,
                80 * scale,
                edible_color,
                180,
                360,
            )
