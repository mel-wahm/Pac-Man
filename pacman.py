from enum import Enum
from math import sin

import arcade

from game_logic import neighbor_coordinates


class Directions(Enum):
    LEFT = "left"
    RIGHT = "right"
    UP = "up"
    DOWN = "down"


DIR_DATA = {
    Directions.UP: (1, 0, -1, 90),
    Directions.RIGHT: (2, 1, 0, 0),
    Directions.DOWN: (4, 0, 1, 270),
    Directions.LEFT: (8, -1, 0, 180),
}


class Pacman:
    def __init__(self, maze):
        self.init_x = (len(maze[0]) - 1) // 2
        self.x = self.init_x
        self.init_y = (len(maze) - 1) // 2
        self.y = self.init_y
        self.prev_x = float(self.x)
        self.prev_y = float(self.y)
        self.smooth_x = float(self.x)
        self.smooth_y = float(self.y)
        self.step_time = 0.0
        self.angle = 0
        self.path = {(self.x, self.y)}
        self.direction = Directions.DOWN
        self.next_direction = Directions.DOWN
        self.maze = maze
        self.death = 0

    def can_turn(self, x, y, direction):
        mask, _, _, _ = DIR_DATA[direction]
        return not (self.maze[y][x] & mask)

    def set_next_direction(self, new_dir):
        self.next_direction = new_dir
        if self.can_turn(self.x, self.y, new_dir):
            self.direction = new_dir
            self.angle = DIR_DATA[new_dir][3]

    def update(self):
        self.prev_x = self.smooth_x
        self.prev_y = self.smooth_y
        self.step_time = 0.0

        cols = len(self.maze[0])
        rows = len(self.maze)
        self.path.add((self.x, self.y))

        if self.can_turn(self.x, self.y, self.next_direction):
            self.direction = self.next_direction

        mask, dx, dy, angle = DIR_DATA[self.direction]
        self.angle = angle

        if not (self.maze[self.y][self.x] & mask):
            self.x = max(0, min(cols - 1, self.x + dx))
            self.y = max(0, min(rows - 1, self.y + dy))

    def smooth_animation(self, delta_time, duration=0.15):
        self.step_time += delta_time
        progress = min(1.0, self.step_time / duration)
        self.smooth_x = self.prev_x + (self.x - self.prev_x) * progress
        self.smooth_y = self.prev_y + (self.y - self.prev_y) * progress

    @property
    def neighbors(self):
        return neighbor_coordinates(self.x, self.y, self.maze)

    def draw(self, renderer):
        cx, cy = renderer.cc(self.smooth_x, self.smooth_y)
        arcade.draw_arc_filled(
            cx,
            cy,
            15 * 0.025 * renderer.cell_size,
            15 * 0.025 * renderer.cell_size,
            arcade.color.YELLOW,
            30 + self.angle + 15 * sin(renderer.progress),
            330 + self.angle - 15 * sin(renderer.progress),
        )
