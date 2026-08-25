import arcade
import json

with open("Src/config/keys.json") as f:
    keys = json.load(f)
keys = {key: getattr(arcade.key, value.split('.')[2]) for key, value in keys.items()}
maze_theme = "ddark"
MAZE_SIZE = (16, 9)
