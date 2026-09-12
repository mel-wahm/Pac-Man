import arcade
from .views import Screen
from .config.parser import ConfigParser


try:
    config = ConfigParser.load()

    window = arcade.Window(1980, 1080, "PACMAN", fullscreen=True)
    start_view = Screen(config)
    window.show_view(start_view)

    try:
        arcade.run()
    except KeyboardInterrupt:
        exit()
except Exception as e:
    print(str(e))
