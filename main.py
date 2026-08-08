import arcade
from screen import Screen

window = arcade.Window(1980, 1080, "PACMAN", fullscreen=True)
start_view = Screen()
window.show_view(start_view)

try:
    arcade.run()
except KeyboardInterrupt:
    exit()
