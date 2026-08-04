import arcade

from mazegenerator import MazeGenerator
from renderer import Render

width = 19
height = 9
maze = MazeGenerator(size=(width, height)).maze
# print(hasattr(arcade, "color"))
Render(maze)
arcade.run()
