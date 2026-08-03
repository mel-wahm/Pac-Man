import arcade

from mazegenerator import MazeGenerator
from renderer import Render
from game_logic import shortest_path
width = 19
height = 7
maze = MazeGenerator(size=(width, height)).maze
# print(hasattr(arcade, "color"))
Render(maze)
arcade.run()
# path = shortest_path((0, 0), (5, 5), maze)


import heapq

lista = [1, 2, 3]

print(heapq.heappop(lista))
print(heapq.heappop(lista))
print(heapq.heappop(lista))
print(heapq.heappop(lista))