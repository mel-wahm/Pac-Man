import arcade

from mazegenerator import MazeGenerator
from renderer import Render
from game_logic import shortest_path, construct_path
width = 19
height = 7
maze = MazeGenerator(size=(width, height)).maze
# print(hasattr(arcade, "color"))
Render(maze)
arcade.run()
# path = shortest_path((0, 0), (5, 5), maze)
# print(path)

s = (0, 0)
e = (5, 5)
print(construct_path(e, s, shortest_path(s, e, maze)))
# print(shortest_path(s, e, maze))