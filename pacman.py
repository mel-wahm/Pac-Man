from enum import Enum
from math import sin

import arcade

from game_logic import neighbor_coordinates


class Directions(Enum):
    LEFT = "left"
    RIGHT = "right"
    UP = "up"
    DOWN = "down"


class Pacman:
    def __init__(self, maze):
        self.x = (len(maze[0]) - 1) // 2
        self.y = (len(maze) - 1) // 2
        self.smooth_x = (len(maze[0]) - 1) // 2
        self.smooth_y = (len(maze) - 1) // 2
        self.angle = 0
        self.path = {(self.x, self.y)}
        self.direction = Directions.DOWN
        self.next_direction = Directions.DOWN
        self.maze = maze

    def can_turn(self, x, y, direction):
        if direction == Directions.UP:
            return not (self.maze[y][x] & 1)
        if direction == Directions.RIGHT:
            return not (self.maze[y][x] & 2)
        if direction == Directions.DOWN:
            return not (self.maze[y][x] & 4)
        if direction == Directions.LEFT:
            return not (self.maze[y][x] & 8)
        return False

    def update(self):
        cols = len(self.maze[0])
        rows = len(self.maze)
        self.path.add((self.x, self.y))
        if self.can_turn(self.x, self.y, self.next_direction):
            self.direction = self.next_direction
        if self.direction == Directions.LEFT:
            if not self.maze[self.y][self.x] & 8:
                self.x = max(self.x - 1, 0)
            self.angle = 180
        if self.direction == Directions.RIGHT:
            if not self.maze[self.y][self.x] & 2:
                self.x = min(self.x + 1, cols - 1)
            self.angle = 0
        if self.direction == Directions.UP:
            if not self.maze[self.y][self.x] & 1:
                self.y = max(self.y - 1, 0)
            self.angle = 90
        if self.direction == Directions.DOWN:
            if not self.maze[self.y][self.x] & 4:
                self.y = min(self.y + 1, rows - 1)
            self.angle = 270
    def	smooth_animation(self, speed, delta_time):
        self.smooth_x += (self.x - self.smooth_x) * speed * delta_time
        self.smooth_y += (self.y - self.smooth_y) * speed * delta_time

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
