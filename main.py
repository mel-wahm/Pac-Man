import arcade


from mazegenerator import MazeGenerator
from game import Game


width = 23
height = 11
maze = MazeGenerator(size=(width, height)).maze
Game(maze)

try:
    arcade.run()
except KeyboardInterrupt:
    exit()
