import arcade

from mazegenerator import MazeGenerator
from renderer import Render

width = 19
height = 7
maze = MazeGenerator(size=(width, height)).maze
Render(maze)
arcade.run()
