import arcade

from mazegenerator import MazeGenerator
from renderer import Render

width = 27
height = 13
maze = MazeGenerator(size=(width, height)).maze

Render(maze)
arcade.run()
