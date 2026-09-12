import arcade


class AudioEngine:
    """Manages audio loading and background sound assets."""

    def __init__(self) -> None:
        self.music = arcade.load_sound("sounds/void_estate.wav", True)
