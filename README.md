*This project has been created as part of the 42 curriculum by tsellak, mel-wahm*

**Description:**
-

In this project, we have created a complete and playable Pac-Man game in Python, using
object-oriented programming, a simple graphical library (arcade), and a modular, reusable architecture


The game supports:

• A custom configuration via a file (JSON with comments) to set game parameters.

• Robust error handling.

• Level generation based on an external ‘A-Maze-ing‘ package.

• A persistent highscore system (stored in a json file on project).

• A polished graphical UI with main menu, game view, and game-over handling.

• A cheat mode for evaluation purposes.

• Deployment to a public gaming platform (Itch.io) for demonstration

**Instructions:**
-

Run:
```bash
make install
make run
```

How to play:

```bash
Moving: W/A/S/D (or other ones based on you liking)
Scoring: Eating gums and super gums and ghosts increases your score
Winning: Eat all pacgums to win a level, and all levels to win the game.
Losing: You lose when your time runs out, or when lose all your lives
```

Other tools:
```bash
make clean: cleans your repository
make lint: runs mypy and flake tests
make debug: runs the game in debug mode
```

**Resources:**
-

```bash
Youtube tutorials:
arcade:
https://www.youtube.com/watch?v=qf47Zqs2xSw&list=PL1P11yPQAo7qgk8uk_A5UxiTrMt6obCc5

movement math:
https://www.youtube.com/watch?v=IwOZV19CH2Y
https://youtu.be/YJB1QnEmlTs?si=ijZ5lCbaCn3W_9XD
```

Ai was mainly used in this project as a guide on how to work with arcade, as there arent much tutorials on this library out there.
It also helped with generating the docstring and the implementation summary in the readme file.


**Configuration:**
-

```py
    "seed": 42, #seed for first level
    "lives": 3, #number of pacman lives
    "level_max_time": 90, #time for each level
    "pacgum": 42, #number of pacgums in each level
    "ghost_step_interval": 0.4, #ghost speed
    "pacman_step_interval": 0.2, #pacman speed
    "ghost.edible_timer": 10.0, #time of ghost being edible
    "ghost.ghost_freeze": 5, #freeze time after ghost spawning
    "points_per_pacgum": 10, #eating pagmus increaes score by this value
    "points_per_super_pacgum": 50, #eating super pagmus increaes score by this value
    "points_per_ghost": 200, #eating ghost increaes score by this value
    "highscore_filename": "src/config/leaderboard.json", # path to json file
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
        {"level": 10, "width": 21, "height": 23},
    ], #size of each level
```

**Highscore:**
-
We sort the score by order, when a new one added, it sorts the new leaderboard by order and keeps the first 10 score.
We used this approach because its the main ones that is used in games.

**General Software Architecture:**
-

The codebase follows a modular, decoupled architecture where presentation, game simulation, entity logic, and data persistence are separated across dedicated modules:

### Modules & Classes Overview

- **Application Entry Point (`pac-man.py`)**:
  - Initializes the fullscreen `arcade.Window` and boots the initial `Screen` view.
- **Views (`src/views/`)**:
  - `Screen`: Title and main navigation hub.
  - `Game`: Central gameplay view managing level progression, dimension scaling, HUD, and delegating simulation.
  - `Settings` & `InGameSettings`: Manage volume, theme, and sub-menu access (in-game or main menu).
  - `Control`: Handles key rebinding with conflict detection and persists mappings to `keys.json`.
  - `Board`: Displays the scrollable top-10 highscores loaded from `leaderboard.json`.
  - `CheatMode`: Toggles global cheat flags (`pacman_inv`, `ghost_freeze`).
  - `Credits`: Displays author credits.
- **Engine (`src/engine/`)**:
  - `GameEngine`: Core game simulation. Owns grid state, spawns actors and dots, runs tick updates, performs collision checks, updates timers, and determines win/loss conditions.
  - `AudioEngine`: Handles background music loading, looping, and volume adjustments.
- **Objects (`src/objects/`)**:
  - `Pacman`: Player actor managing buffered direction turns, portal wrapping, position interpolation, and mouth animations.
  - `Ghost`: Enemy AI actors managing state transitions (chase, evasion, wandering) and procedural sprite rendering.
- **Core (`src/core/`)**:
  - `Directions` / `DIR_DATA`: Enum and bitmask mappings (1, 2, 4, 8) for grid directions and maze walls.
  - `pathfinding`: Stateless Breadth-First Search (BFS) utilities (`shortest_path`, `construct_path`, `neighbor_coordinates`).
- **Configuration & Storage (`src/config/`)**:
  - `ConfigParser`: Strips comments, parses, validates, and clamps `config.json` against safe defaults.
  - `theme.py`: Palette dictionary defining color mappings for dark and light modes.
- **UI Components (`src/ui/`)**:
  - Reusable menu and widget controls (`Menu`, `Selection`, `AudioControl`, `ThemeToggle`).

### Class Relationships & Data Flow


1. **View Flow**: `arcade.Window` switches active `arcade.View` instances depending on game state.
2. **Simulation**: `Game` handles player keyboard events and frame ticks, delegating all physics and entity states to `GameEngine`.
3. **Actor Interactions**: `GameEngine` updates `Pacman` and the 4 `Ghost` actors. Ghosts query `pathfinding` functions to plot paths toward or away from `Pacman`.
4. **Data Persistence**: `ConfigParser` feeds validated settings to `Game` and `GameEngine`, while UI views persist user settings back to JSON (`keys.json`, `options.json`, `leaderboard.json`).

**Implementation:**
-

The game is built with Python 3.12 and the Python Arcade library, structured around a modular, object-oriented architecture:

- **Architecture & View Management**:
  - Organized into distinct modules: `core` (directions, bitmasks, BFS pathfinding), `objects` (Pac-Man and Ghost entities), `engine` (game loop physics, collision, timers, audio), `config` (parser, theming, persistent state), `ui` (reusable menu widgets), and `views` (Arcade view state machine).
  - Uses Arcade's `View` management to transition between views: Title Screen (`Screen`), Gameplay (`Game`), Pause / Options (`InGameSettings`, `Settings`), Rebinding (`Control`), Highscores (`Board`), Cheats (`CheatMode`), and Credits (`Credits`).

- **Grid System & Pathfinding**:
  - Mazes are generated per level using bitmask encoding for walls (`1: UP`, `2: RIGHT`, `4: DOWN`, `8: LEFT`).
  - Implements Breadth-First Search (BFS) pathfinding (`src/core/pathfinding.py`) operating over the bitmasked maze graph to compute shortest paths.
  - Dynamic viewport scaling automatically fits mazes of varying dimensions while reserving HUD sidebar space.
  - Supports wrap-around warp tunnels on all four perimeter edges.

- **Actor Mechanics & Ghost AI**:
  - **Pac-Man (`Pacman`)**: Direction buffering (`set_next_direction` / `can_turn`), warp tunnel teleportation, delta-time linear coordinate interpolation (`smooth_animation`) between discrete grid steps, and procedural mouth-arc chomp rendering.
  - **Ghosts (`Ghost`)**: Multi-state AI behavior:
    - *Chase*: Tracks and follows the BFS shortest path to Pac-Man when in range.
    - *Frightened / Edible*: Triggers upon eating a Super Pacgum; ghosts navigate to tiles maximizing Euclidean distance from Pac-Man, flashing as the edible timer runs out.
    - *Wander*: Explores corridors randomly when distant without making immediate 180° reversals.
    - Features spawn freeze delays, eaten respawn logic, and procedural rendering (body arcs, animated wavy skirt, pupil gaze tracking, and sinusoidal mouth).

- **Configuration, Error Handling & Persistence**:
  - `ConfigParser` strips `#` comments from JSON, validates types and ranges, and clamps parameters (e.g., maze dimensions clamped between 8 and 40) with fallback to `SAFE_DEFAULTS`.
  - Persistent JSON storage for sorted top-10 highscores (`leaderboard.json`), rebindable controls (`keys.json`), and user preferences (`options.json`).

- **Theming & Audio**:
  - Dual-theme support (`dark` and `light`) altering palettes for walls, outlines, center "42" blocks, dots, actors, and HUD elements.
  - Background music streaming and volume adjustment handled through `AudioEngine`.

**Project management:**
-

We split work by domain — visualization/logic and parsing/error handling — and tracked
progress and risks as we went. Full details (timeline, risk analysis, test plan, team
organization) are in `docs/project-management/team_management.md`.


**Maze Generation:**
-

We use the assigned A-Maze-ing package with `PERFECT` set to `False`, producing
Pac-Man-compatible corridors (loops, not a strict tree) instead of a perfect maze.

We instantiate the generator as `Maze(width, height, seed)` and read `maze.maze`, a
2D array of numbers representing the grid. Our loader adapts to this interface directly —
we don't modify the package, we just convert its output into the wall/corridor
representation our engine expects.

Only the first level is seeded (fixed seed, e.g. 42) for a reproducible starting maze;
every subsequent level generates a new maze with no seed, so it's randomized each run.

Width and height are clamped to a minimum and maximum in our config validation, to
avoid triggering a recursion error in the generator on invalid or extreme dimensions.

---