import arcade


class AudioEngine:
    def __init__(self) -> None:
        self.music = arcade.load_sound("sounds/void_estate.wav", True)
