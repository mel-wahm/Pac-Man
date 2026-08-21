from math import hypot
from random import sample

import arcade

from ..core import Directions
from ..objects import Ghost, Pacman


class GameEngine:
    """Core Game Engine: handles maze state, entity management, physics, and game rules."""

    def __init__(self, maze: list, center_func, cell_size: float):
        self.center = center_func
        self.cell_size = cell_size
        self.super_gum_textures = [
            arcade.load_texture("fruits/super_fruit_yellow.png"),
            arcade.load_texture("fruits/super_fruit_pink.png"),
            arcade.load_texture("fruits/super_fruit_cyan.png"),
            arcade.load_texture("fruits/super_fruit_green.png"),
        ]

        # Open warp tunnels on the 4 border edges
        maze[0][len(maze[0]) // 2] -= 1
        maze[len(maze) - 1][len(maze[0]) // 2] -= 4
        maze[len(maze) // 2][0] -= 8
        maze[len(maze) // 2][len(maze[0]) - 1] -= 2

        self.maze = maze
        self.cols = len(self.maze[0])
        self.rows = len(self.maze)
        self.half_width = (self.cols - 1) / 2
        self.half_height = (self.rows - 1) / 2

        self.pacman = Pacman(maze)
        self.max_dots = 1000
        self.state = 0
        self.pause = 0
        self.progress = 0
        self.elapsed_time = 0.0
        self.ghost_step_timer = 0.0
        self.pacman_step_timer = 0.0
        self.win_timer = 0.0

        self.corners = {
            (0, 0),
            (self.cols - 1, 0),
            (0, self.rows - 1),
            (self.cols - 1, self.rows - 1),
        }

        self.ghosts = {
            Ghost(
                (0, 0),
                self.center(0, 0),
                self.maze,
                (255, 0, 0),
                self.cell_size,
            ),
            Ghost(
                (self.cols - 1, 0),
                self.center(self.cols - 1, 0),
                self.maze,
                (255, 184, 255),
                self.cell_size,
            ),
            Ghost(
                (0, self.rows - 1),
                self.center(0, self.rows - 1),
                self.maze,
                (0, 255, 255),
                self.cell_size,
            ),
            Ghost(
                (self.cols - 1, self.rows - 1),
                self.center(self.cols - 1, self.rows - 1),
                self.maze,
                (255, 184, 82),
                self.cell_size,
            ),
        }

        self.forty_two_coords = set()
        if self.rows >= 10 and self.cols >= 14:
            mid_x = (self.cols - 7) // 2
            mid_y = (self.rows - 5) // 2
            self.forty_two_coords = {
                (mid_x + 0, mid_y + 0),
                (mid_x + 4, mid_y + 0),
                (mid_x + 5, mid_y + 0),
                (mid_x + 6, mid_y + 0),
                (mid_x + 0, mid_y + 1),
                (mid_x + 6, mid_y + 1),
                (mid_x + 0, mid_y + 2),
                (mid_x + 1, mid_y + 2),
                (mid_x + 2, mid_y + 2),
                (mid_x + 4, mid_y + 2),
                (mid_x + 5, mid_y + 2),
                (mid_x + 6, mid_y + 2),
                (mid_x + 2, mid_y + 3),
                (mid_x + 4, mid_y + 3),
                (mid_x + 2, mid_y + 4),
                (mid_x + 4, mid_y + 4),
                (mid_x + 5, mid_y + 4),
                (mid_x + 6, mid_y + 4),
            }

        self.wall_lines = []
        self.dots = arcade.SpriteList()
        self.dots_grid = {}
        self.valid_dot_coords = []

        for r in range(self.rows):
            for c in range(self.cols):
                real_x, real_y = self.center(c, r)
                half = self.cell_size / 2
                cell_val = self.maze[r][c]

                if cell_val & 1:
                    self.wall_lines.extend(
                        [
                            (real_x - half, real_y + half),
                            (real_x + half, real_y + half),
                        ]
                    )
                if cell_val & 2:
                    self.wall_lines.extend(
                        [
                            (real_x + half, real_y + half),
                            (real_x + half, real_y - half),
                        ]
                    )
                if cell_val & 4:
                    self.wall_lines.extend(
                        [
                            (real_x - half, real_y - half),
                            (real_x + half, real_y - half),
                        ]
                    )
                if cell_val & 8:
                    self.wall_lines.extend(
                        [
                            (real_x - half, real_y + half),
                            (real_x - half, real_y - half),
                        ]
                    )

                if (
                    (c, r) not in self.forty_two_coords
                    and (c, r) not in self.pacman.path
                    and (c, r) not in self.corners
                ):
                    self.valid_dot_coords.append((c, r))

        self.spawned_dot_coords = sample(
            self.valid_dot_coords, min(len(self.valid_dot_coords), self.max_dots)
        )
        for cell in self.spawned_dot_coords:
            c, r = cell
            real_x, real_y = self.center(c, r)
            dot_r = int(self.cell_size * 0.05)
            dot = arcade.SpriteCircle(radius=max(1, dot_r), color=(255, 255, 0))
            dot.center_x = real_x
            dot.center_y = real_y
            self.dots.append(dot)
            self.dots_grid[(c, r)] = dot

        for i, cell in enumerate(sorted(self.corners)):
            c, r = cell
            real_x, real_y = self.center(c, r)
            super_gum = arcade.Sprite(self.super_gum_textures[i % 4])
            super_gum.width = self.cell_size * 0.6
            super_gum.height = self.cell_size * 0.6
            super_gum.center_x = real_x
            super_gum.center_y = real_y
            self.dots.append(super_gum)
            self.dots_grid[(c, r)] = super_gum

    def reset_game(self):
        self.state = 0
        self.pause = 0
        self.elapsed_time = 0.0
        self.progress = 0
        self.ghost_step_timer = 0.0
        self.pacman_step_timer = 0.0
        self.win_timer = 0.0

        self.pacman.reset_game()

        for g in self.ghosts:
            g.reset_game()

        self.dots = arcade.SpriteList()
        self.dots_grid = {}
        self.spawned_dot_coords = sample(
            self.valid_dot_coords, min(len(self.valid_dot_coords), self.max_dots)
        )
        for cell in self.spawned_dot_coords:
            c, r = cell
            real_x, real_y = self.center(c, r)
            dot_r = int(self.cell_size * 0.05)
            dot = arcade.SpriteCircle(radius=dot_r, color=(255, 255, 0))
            dot.center_x = real_x
            dot.center_y = real_y
            self.dots.append(dot)
            self.dots_grid[(c, r)] = dot

        for i, cell in enumerate(sorted(self.corners)):
            c, r = cell
            real_x, real_y = self.center(c, r)
            super_gum = arcade.Sprite(self.super_gum_textures[i % 4])
            super_gum.width = self.cell_size * 0.6
            super_gum.height = self.cell_size * 0.6
            super_gum.center_x = real_x
            super_gum.center_y = real_y
            self.dots.append(super_gum)
            self.dots_grid[(c, r)] = super_gum

    def update(self, delta_time):
        ghost_speed_rate = 8
        pacman_step_interval = 0.14

        if len(self.dots) == 0:
            self.pause = 1
            self.state = 3

        if self.state == 3:
            self.win_timer = min(1.0, self.win_timer + delta_time * 2.0)

        for ghost in self.ghosts:
            distance_to_pacman = hypot(
                (ghost.smooth_x - self.pacman.smooth_x),
                (ghost.smooth_y - self.pacman.smooth_y),
            )
            if distance_to_pacman < 0.5:
                if not ghost.edible:
                    self.pacman.death_count += 1
                    self.pacman.x = self.pacman.init_x
                    self.pacman.smooth_x = float(self.pacman.init_x)
                    self.pacman.y = self.pacman.init_y
                    self.pacman.smooth_y = float(self.pacman.init_y)
                    self.pacman.prev_x = float(self.pacman.init_x)
                    self.pacman.prev_y = float(self.pacman.init_y)
                    self.pacman.direction = Directions.DOWN
                    self.pacman.next_direction = Directions.DOWN
                    for g in self.ghosts:
                        g.edible_timer = 0.0
                        g.edible = False
                        g.grid_pos = g.spawn_pos
                        g.path = []
                        g.smooth_x = float(g.spawn_pos[0])
                        g.smooth_y = float(g.spawn_pos[1])
                        g.draw_coords = self.center(g.smooth_x, g.smooth_y)
                        g.ghost_freeze = 1
                    if self.pacman.death_count == 3:
                        self.reset_game()
                        self.state = 1
                        self.pause = 1
                        self.pacman.death_count = 0
                        self.pacman.path = {(self.pacman.x, self.pacman.y)}
                    break
                else:
                    self.pacman.score += 100
                    self.pacman.score_text.text = f"SCORE: {self.pacman.score}"
                    ghost.grid_pos = ghost.spawn_pos
                    ghost.smooth_x = float(ghost.spawn_pos[0])
                    ghost.smooth_y = float(ghost.spawn_pos[1])
                    ghost.draw_coords = self.center(ghost.smooth_x, ghost.smooth_y)
                    ghost.ghost_freeze = 5
                    ghost.edible_timer = 0.0
                    ghost.edible = False
                    break

        if not self.pause:
            self.elapsed_time += delta_time
            self.progress += 6 * delta_time
            self.ghost_step_timer += delta_time
            self.pacman_step_timer += delta_time

            should_choose_target = False
            if self.ghost_step_timer > 2.5 / ghost_speed_rate:
                self.ghost_step_timer = 0.0
                should_choose_target = True

            for ghost in self.ghosts:
                ghost.ghost_freeze -= delta_time
                if ghost.ghost_freeze <= 0:
                    if should_choose_target:
                        ghost.choose_target(self.pacman)
                    ghost.update(ghost_speed_rate, delta_time)
                    ghost.draw_coords = self.center(ghost.smooth_x, ghost.smooth_y)

            if self.pacman_step_timer > pacman_step_interval:
                self.pacman_step_timer = 0.0
                self.pacman.update()
            if not self.pacman.is_teleporting:
                self.pacman.smooth_animation(delta_time, pacman_step_interval)

            smooth_cell = (
                self.pacman.smooth_x,
                self.pacman.smooth_y,
            )
            if smooth_cell in self.dots_grid:
                self.pacman.score += 10
                self.pacman.score_text.text = f"SCORE: {self.pacman.score}"
                dot = self.dots_grid.pop(smooth_cell)
                if smooth_cell in self.corners:
                    for ghost in self.ghosts:
                        ghost.edible = True
                        ghost.edible_timer = 8.0
                dot.remove_from_sprite_lists()
