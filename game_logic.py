from collections import deque
from enum import Enum


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


def neighbor_coordinates(x, y, maze):
    neighbors = []
    c = len(maze[0]) - 1
    r = len(maze) - 1
    if x and not maze[y][x] & 8:
        neighbors.append((x - 1, y))
    if y and not maze[y][x] & 1:
        neighbors.append((x, y - 1))
    if x < c and not maze[y][x] & 2:
        neighbors.append((x + 1, y))
    if y < r and not maze[y][x] & 4:
        neighbors.append((x, y + 1))
    return neighbors


def center_coordinates(x, y, width, height, total_w, total_h, cell_size):
    nx = width / 2 + (x - total_w) * cell_size
    ny = height / 2 - (y - total_h) * cell_size
    return (nx, ny)


def shortest_path(start, end, maze):
    px, py = start
    ex, ey = end
    final_path = {}
    queue = deque()
    queue.append((px, py))
    visited = set()
    visited.add((px, py))
    while queue:
        cx, cy = queue.popleft()
        for nx, ny in neighbor_coordinates(cx, cy, maze):
            if (nx, ny) in visited:
                continue
            visited.add((nx, ny))
            queue.append((nx, ny))
            final_path[(nx, ny)] = (cx, cy)
            if (nx, ny) == (ex, ey):
                return final_path


def construct_path(end, start, final):
    ex, ey = end
    sx, sy = start
    final_path = []
    final_path.append(end)
    while (ex, ey) != start:
        ex, ey = final[(ex, ey)]
        final_path.append((ex, ey))
    return final_path[::-1]
