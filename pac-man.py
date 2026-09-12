import arcade
import sys
from src.views import Screen
from src.config.parser import ConfigParser


def main() -> None:
    try:
        config = ConfigParser.load()

        window = arcade.Window(1080, 720, "PACMAN", fullscreen=True)
        start_view = Screen(config)
        window.show_view(start_view)

        try:
            arcade.run()
        except KeyboardInterrupt:
            sys.exit(0)
    except Exception as e:
        print(str(e))
        sys.exit(1)


if __name__ == "__main__":
    main()
