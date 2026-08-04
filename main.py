import arcade

from mazegenerator import MazeGenerator
from game import Game

width = 19
height = 7
maze = MazeGenerator(size=(width, height)).maze
Game(maze)
arcade.run()
