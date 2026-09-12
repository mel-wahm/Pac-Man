import arcade
import json
import sys
from typing import Any, Dict

MAZE_SIZE = (9, 11)
pacman_inv = False
ghost_freeze = False


def load_keys() -> Dict[str, int]:
    """Load key binding configurations from JSON file.

    Returns:
        Dictionary mapping directional action names to arcade key codes.

    Raises:
        ValueError: If key mappings are missing or invalid.
    """
    try:
        key_path = "src/config/keys.json"
        with open(key_path) as f:
            keys = json.load(f)
        keys = {
            key: getattr(arcade.key, value.split(".")[2])
            for key, value in keys.items()
            }
        allow_list = ["UP", "DOWN", "LEFT", "RIGHT"]

        if len(keys) != len(allow_list):
            raise ValueError(f"The file '{key_path}' is not Valid.")

        for key in keys:
            if key not in allow_list:
                raise ValueError(f"The Key: '{key}' not Valid.")

        return keys
    except FileNotFoundError:
        print(f"Error: File '{key_path}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error loading keys: {e}")
        sys.exit(1)


keys = load_keys()


SAFE_DEFAULTS: Dict[str, Any] = {
    "seed": 42,
    "lives": 3,
    "level_max_time": 90,
    "pacgum": 42,
    "ghost_step_interval": 0.4,
    "pacman_step_interval": 0.2,
    "ghost.edible_timer": 10.0,
    "ghost.ghost_freeze": 5,
    "points_per_pacgum": 10,
    "points_per_super_pacgum": 50,
    "points_per_ghost": 200,
    "highscore_filename": "src/config/leaderboard.json",
    "levels": [
        {"level": 1, "width": 9, "height": 11},
        {"level": 2, "width": 11, "height": 13},
        {"level": 3, "width": 13, "height": 15},
        {"level": 4, "width": 15, "height": 17},
        {"level": 5, "width": 15, "height": 17},
        {"level": 6, "width": 17, "height": 19},
        {"level": 7, "width": 17, "height": 19},
        {"level": 8, "width": 19, "height": 21},
        {"level": 9, "width": 19, "height": 21},
        {"level": 10, "width": 21, "height": 23}
    ]
}


class ConfigParser:
    """Parser and validator for Pac-Man game configuration files."""

    @classmethod
    def load(cls) -> Dict[str, Any]:
        """Parse, validate, and return game configuration settings.

        Reads the JSON configuration file specified in command-line arguments,
        strips comments, validates value types/bounds, and supplies defaults.

        Returns:
            Dictionary of validated game configuration parameters.

        Raises:
            ValueError: If command line arguments or config values are invalid.
            FileNotFoundError: If the specified configuration file is missing.
        """
        try:
            len_args = len(sys.argv)
            if len_args != 2:
                cmd = " ".join(sys.argv)
                raise ValueError(
                    "Expected: python3 pac-man.py config.json\n"
                    f"Got: python3 {cmd}"
                )
            filepath = sys.argv[-1]

            if not filepath.endswith(".json"):
                raise FileExistsError(
                    f"[Config Warning] File '{filepath}' does not have a "
                    ".json extension."
                )

            try:
                with open(filepath, "r") as f:
                    content = f.read()
                    if not content.strip():
                        raise ValueError("Error: The file is empty.")
            except FileNotFoundError:
                raise FileNotFoundError(f"Error: File '{filepath}' not found.")

            clean_lines: list[str] = []
            for line in content.splitlines():
                if "#" in line:
                    line = line.split("#")[0]
                if not line.strip():
                    continue
                clean_lines.append(line)

            clean_json = "\n".join(clean_lines)
            try:
                data = json.loads(clean_json)
                if not isinstance(data, dict):
                    print(
                        "[Config Warning] Root JSON must be an object. "
                        "Falling back to defaults."
                    )
                    return SAFE_DEFAULTS.copy()
            except json.JSONDecodeError as e:
                print(
                    f"[Config Warning] Invalid JSON format ({e}). "
                    "Falling back to defaults."
                )
                return SAFE_DEFAULTS.copy()

            config: Dict[str, Any] = SAFE_DEFAULTS.copy()

            def clamped_message(key: str, invalid: bool) -> str:
                if invalid:
                    return (
                        f"[Config Warning] Invalid {key} value "
                        f"({data.get(key)}). Clamped to {config.get(key)}."
                    )
                else:
                    return (
                        f"[Config Warning] Missing key '{key}'. "
                        f"Using default value: {config.get(key)}."
                    )

            numeric_rules: Dict[str, tuple[Any, float]] = {
                "lives": (int, 1),
                "level_max_time": ((int, float), 1),
                "pacgum": (int, 1),
                "ghost_step_interval": ((int, float), 0.05),
                "pacman_step_interval": ((int, float), 0.05),
                "ghost.edible_timer": ((int, float), 1.0),
                "ghost.ghost_freeze": ((int, float), 1.0),
                "seed": (int, 0),
                "points_per_pacgum": (int, 0),
                "points_per_super_pacgum": (int, 0),
                "points_per_ghost": (int, 0),
            }

            for key, (t_type, min_val) in numeric_rules.items():
                if key in data:
                    val = data[key]
                    if (
                        isinstance(val, t_type)
                        and not isinstance(val, bool)
                        and val >= min_val
                    ):
                        config[key] = val
                    else:
                        print(clamped_message(key, True))
                else:
                    print(clamped_message(key, False))

            key = "levels"
            if (
                key in data
                and isinstance(data[key], list)
                and len(data[key]) > 0
            ):
                validated_levels: list[dict[str, int]] = []

                for idx, level in enumerate(data[key], start=1):
                    if not isinstance(level, dict):
                        print(
                            f"[Config Warning] Level at index {idx} "
                            "is invalid. Skipped."
                        )
                        continue

                    lvl_num = level.get("level", idx)
                    if (
                        not isinstance(lvl_num, int)
                        or isinstance(lvl_num, bool)
                        or lvl_num < 1
                    ):
                        lvl_num = idx

                    w = level.get("width")
                    if isinstance(w, int) and not isinstance(w, bool):
                        if w < 8:
                            print(
                                f"[Config Warning] Level {lvl_num} width "
                                f"({w}) is too small. Clamped to 8."
                            )
                            w = 8
                        elif w > 40:
                            print(
                                f"[Config Warning] Level {lvl_num} width "
                                f"({w}) is too large. Clamped to 40."
                            )
                            w = 40
                    else:
                        print(
                            f"[Config Warning] Level {lvl_num} has "
                            f"invalid width ({w}). Defaulted to 9."
                        )
                        w = 9

                    h = level.get("height")
                    if isinstance(h, int) and not isinstance(h, bool):
                        if h < 8:
                            print(
                                f"[Config Warning] Level {lvl_num} height "
                                f"({h}) is too small. Clamped to 8."
                            )
                            h = 8
                        elif h > 40:
                            print(
                                f"[Config Warning] Level {lvl_num} height "
                                f"({h}) is too large. Clamped to 40."
                            )
                            h = 40
                    else:
                        print(
                            f"[Config Warning] Level {lvl_num} has "
                            f"invalid height ({h}). Defaulted to 11."
                        )
                        h = 11

                    validated_levels.append(
                        {"level": idx, "width": w, "height": h}
                    )

                if validated_levels:
                    config["levels"] = validated_levels
                else:
                    print(
                        "[Config Warning] No valid levels in config. "
                        "Using safe defaults."
                    )
            else:
                print(clamped_message(key, False))

            if "highscore_filename" in data:
                h_file = data["highscore_filename"]
                if isinstance(h_file, str) and h_file.strip():
                    if h_file.startswith("Src/"):
                        h_file = "src/" + h_file[4:]
                    config["highscore_filename"] = h_file
            return config

        except Exception as e:
            raise Exception(e)
