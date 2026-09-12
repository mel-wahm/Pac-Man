from .parser import (
    ConfigParser,
    MAZE_SIZE,
    ghost_freeze,
    keys,
    pacman_inv,
)
from . import parser
from .theme import THEMES

__all__ = [
    "ConfigParser",
    "MAZE_SIZE",
    "THEMES",
    "parser",
    "ghost_freeze",
    "keys",
    "pacman_inv",
]
