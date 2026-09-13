
# **Project management:**
**Team Organization**

- **mel-wahm**: handled the visualizing and logic
- **tsellak**: handled the parsing and error handling

**Timeline**

Started ~1 month before pushing. Rough order of work:

1. Maze rendering
2. Drawing ghosts and Pac-Man
3. Movement logic for player/ghosts
4. Menu
5. Game logic
6. Parsing
7. Error handling

**Risks / Blocking Points**

- **Performance**: Python is slow, ran into latency issues that needed optimization.
- **Late constraint change**: we struggeled to only use methods that are available in MLX.

**Arcade → MLX Function Mapping**

| Arcade Function | Closest MLX Equivalent |
|---|---|
| `arcade.run` | `mlx_loop()` |
| `arcade.load_texture` | `mlx_xpm_file_to_image()` |
| `arcade.draw_texture_rect` | `mlx_put_image_to_window()` |
| `arcade.draw_circle_filled` | `mlx_pixel_put()` (looped) |
| `arcade.draw_arc_filled` | `mlx_pixel_put()` (looped) |
| `arcade.draw_line_strip` | `mlx_pixel_put()` (looped) |
| `arcade.draw_lines` | `mlx_pixel_put()` (looped) |
| `arcade.draw_rect_filled` | `mlx_pixel_put()` (looped) |

**Acceptance Test Plan**

Manual testing throughout development. Notable bugs found/fixed:

- Double death triggering when a ghost touches the player
- Config error handling (many edge cases)
- Unsupported key bindings

**Project Analysis**

- **Graphics library (Arcade)**: chosen out of interest in game development — Arcade seemed like a good fit for building a full 2D game with sprites, views, and audio support.
