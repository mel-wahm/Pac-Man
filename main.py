import arcade

from mazegenerator import MazeGenerator
from game import Game


width = 11
height = 7
maze = MazeGenerator(size=(width, height)).maze
Game(maze)

try:
    arcade.run()
except KeyboardInterrupt:
    exit()
