import arcade

from mazegenerator import MazeGenerator
from game import Game

width = 9
height = 4
maze = MazeGenerator(size=(width, height)).maze
Game(maze)
arcade.run()
