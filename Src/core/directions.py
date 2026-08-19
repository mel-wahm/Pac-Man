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
