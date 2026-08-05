import arcade

from mazegenerator import MazeGenerator
from game import Game

width = 17
height = 9
maze = MazeGenerator(size=(width, height)).maze
Game(maze)
arcade.run()
