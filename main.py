import arcade

from mazegenerator import MazeGenerator
from renderer import Render
from game_logic import shortest_path, construct_path

width = 19
height = 9
maze = MazeGenerator(size=(width, height)).maze
# print(hasattr(arcade, "color"))
Render(maze)
arcade.run()
