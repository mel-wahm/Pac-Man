from math import hypot
import arcade

from game_logic import center_coordinates
from ghost import Ghost
from pacman import Directions, Pacman


class Game(arcade.Window):
    def __init__(self, maze: list):
        super().__init__(1980, 1080, "PACMAN", True, True, vsync=False)
        self.background_color = (10, 10, 30)
        self.state = 0
        self.maze = maze
        self.pacman = Pacman(maze)
        self.total_w = (len(self.maze[0]) - 1) / 2
        self.total_h = (len(self.maze) - 1) / 2
        self.drag_x = 0
        self.drag_y = 0
        self.cols = len(self.maze[0])
        self.rows = len(self.maze)
        self.progress = 0
        self.sec = 0
        self.ghost_speed = 0
        self.pacman_speed = 0
        self.seconds = 0
        self.pause = 0
        cx = self.width / 2
        cy = self.height / 2
        self.pause_text = arcade.Text(
            "PAUSE",
            cx,
            cy,
            (200, 200, 200),
            font_size=60,
            anchor_x="center",
            anchor_y="center",
            bold=True,
        )
        self.died_text = arcade.Text(
            "YOU DIED",
            cx,
            cy,
            (180, 15, 15),
            font_size=80,
            anchor_x="center",
            anchor_y="center",
            bold=True,
        )
        self.won_text = arcade.Text(
            "YOU WON",
            cx,
            cy,
            (255, 200, 0),
            font_size=80,
            anchor_x="center",
            anchor_y="center",
            bold=True,
        )
        self.cell_size = min(
            (self.width - 150) / self.cols, (self.height - 150) / self.rows
        )
        self.corners = {
            (0, 0),
            (self.cols - 1, 0),
            (0, self.rows - 1),
            (self.cols - 1, self.rows - 1),
        }
        self.ghosts = {
            Ghost(
                (0, 0),
                self.cc(0, 0),
                self.maze,
                (255, 0, 0),
                self.cell_size,
            ),
            Ghost(
                (self.cols - 1, 0),
                self.cc(self.cols - 1, 0),
                self.maze,
                (255, 184, 255),
                self.cell_size,
            ),
            Ghost(
                (0, self.rows - 1),
                self.cc(0, self.rows - 1),
                self.maze,
                (0, 255, 255),
                self.cell_size,
            ),
            Ghost(
                (self.cols - 1, self.rows - 1),
                self.cc(self.cols - 1, self.rows - 1),
                self.maze,
                (255, 184, 82),
                self.cell_size,
            ),
        }
        self.forty_two_coords = set()
        if self.rows >= 10 and self.cols >= 14:
            _42_x = (self.cols - 7) // 2
            _42_y = (self.rows - 5) // 2
            self.forty_two_coords = {
                (_42_x + 0, _42_y + 0),
                (_42_x + 4, _42_y + 0),
                (_42_x + 5, _42_y + 0),
                (_42_x + 6, _42_y + 0),
                (_42_x + 0, _42_y + 1),
                (_42_x + 6, _42_y + 1),
                (_42_x + 0, _42_y + 2),
                (_42_x + 1, _42_y + 2),
                (_42_x + 2, _42_y + 2),
                (_42_x + 4, _42_y + 2),
                (_42_x + 5, _42_y + 2),
                (_42_x + 6, _42_y + 2),
                (_42_x + 2, _42_y + 3),
                (_42_x + 4, _42_y + 3),
                (_42_x + 2, _42_y + 4),
                (_42_x + 4, _42_y + 4),
                (_42_x + 5, _42_y + 4),
                (_42_x + 6, _42_y + 4),
            }

        self.wall_thickness = max(1, int(self.cell_size * 0.03))
        self.wall_lines = []
        self.dots = arcade.SpriteList()
        self.dots_grid = {}

        for r in range(self.rows):
            for c in range(self.cols):
                real_x, real_y = self.cc(c, r)
                half = self.cell_size / 2
                cell_val = self.maze[r][c]

                if cell_val & 1:
                    self.wall_lines.extend([(real_x - half, real_y + half), (real_x + half, real_y + half)])
                if cell_val & 2:
                    self.wall_lines.extend([(real_x + half, real_y + half), (real_x + half, real_y - half)])
                if cell_val & 4:
                    self.wall_lines.extend([(real_x - half, real_y - half), (real_x + half, real_y - half)])
                if cell_val & 8:
                    self.wall_lines.extend([(real_x - half, real_y + half), (real_x - half, real_y - half)])

                if (c, r) not in self.forty_two_coords and (c, r) not in self.pacman.path:
                    dot_r = max(1, int(self.cell_size * (0.125 if (c, r) in self.corners else 0.05)))
                    dot = arcade.SpriteCircle(radius=dot_r, color=(255, 255, 0))
                    dot.center_x = real_x
                    dot.center_y = real_y
                    self.dots.append(dot)
                    self.dots_grid[(c, r)] = dot

    def reset_game(self):
        self.state = 0
        self.pause = 0
        self.sec = 0
        self.progress = 0
        self.ghost_speed = 0
        self.pacman_speed = 0

        self.pacman.death = 0
        self.pacman.x = self.pacman.init_x
        self.pacman.y = self.pacman.init_y
        self.pacman.smooth_x = float(self.pacman.init_x)
        self.pacman.smooth_y = float(self.pacman.init_y)
        self.pacman.prev_x = float(self.pacman.init_x)
        self.pacman.prev_y = float(self.pacman.init_y)
        self.pacman.direction = Directions.DOWN
        self.pacman.next_direction = Directions.DOWN
        self.pacman.path = {(self.pacman.init_x, self.pacman.init_y)}

        for g in self.ghosts:
            g.r_c = g.default
            g.smooth_x = float(g.default[0])
            g.smooth_y = float(g.default[1])
            g.path = []
            g.draw_cords = self.cc(g.smooth_x, g.smooth_y)

        self.dots = arcade.SpriteList()
        self.dots_grid = {}
        for r in range(self.rows):
            for c in range(self.cols):
                if (c, r) not in self.forty_two_coords and (c, r) not in self.pacman.path:
                    real_x, real_y = self.cc(c, r)
                    dot_r = max(1, int(self.cell_size * (0.125 if (c, r) in self.corners else 0.05)))
                    dot = arcade.SpriteCircle(radius=dot_r, color=(255, 255, 0))
                    dot.center_x = real_x
                    dot.center_y = real_y
                    self.dots.append(dot)
                    self.dots_grid[(c, r)] = dot

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.LEFT:
            self.pacman.set_next_direction(Directions.LEFT)
        if symbol == arcade.key.RIGHT:
            self.pacman.set_next_direction(Directions.RIGHT)
        if symbol == arcade.key.UP:
            self.pacman.set_next_direction(Directions.UP)
        if symbol == arcade.key.DOWN:
            self.pacman.set_next_direction(Directions.DOWN)
        if symbol == arcade.key.F:
            self.set_fullscreen(not self.fullscreen)
        if symbol == arcade.key.R:
            self.reset_game()
        if symbol == arcade.key.SPACE:
            self.state = 2
            self.pause = not (self.pause)
        if symbol == arcade.key.Q:
            exit(0)

    def cc(self, x, y):
        return center_coordinates(
            x,
            y,
            self.width,
            self.height,
            self.total_w,
            self.total_h,
            self.cell_size,
        )

    def on_update(self, delta_time):
        if len(self.dots) == 0:
            self.pause = 1
            self.state = 3

        for ghost in self.ghosts:
            if (
                hypot(
                    (ghost.smooth_x - self.pacman.smooth_x),
                    (ghost.smooth_y - self.pacman.smooth_y),
                )
                < 0.5
            ):
                self.pacman.death += 1
                self.pacman.x = self.pacman.init_x
                self.pacman.smooth_x = self.pacman.init_x
                self.pacman.y = self.pacman.init_y
                self.pacman.smooth_y = self.pacman.init_y
                self.pacman.prev_x = self.pacman.init_x
                self.pacman.prev_y = self.pacman.init_y
                self.pacman.direction = Directions.DOWN
                self.pacman.next_direction = Directions.DOWN
                for g in self.ghosts:
                    g.r_c = g.default
                    g.path = []
                    g.smooth_x = float(g.default[0])
                    g.smooth_y = float(g.default[1])
                    g.draw_cords = self.cc(g.smooth_x, g.smooth_y)
                if self.pacman.death == 3:
                    self.reset_game()
                    self.state = 1
                    self.pause = 1
                    self.pacman.death = 0
                    self.pacman.path = {(self.pacman.x, self.pacman.y)}
                break

        if not self.pause:
            self.sec += delta_time
            self.progress += 6 * delta_time
            self.ghost_speed += delta_time
            self.pacman_speed += delta_time

            speed = 6
            if self.ghost_speed > 2.5 / speed:
                self.ghost_speed = 0
                for ghost in self.ghosts:
                    ghost.choose_target(self.pacman)

            for ghost in self.ghosts:
                ghost.update(speed, delta_time)
                ghost.draw_cords = self.cc(ghost.smooth_x, ghost.smooth_y)
            duration = 0.15
            if self.pacman_speed > duration:
                self.pacman_speed = 0
                self.pacman.update()
            self.pacman.smooth_animation(delta_time, duration)

            smooth_cell = (round(self.pacman.smooth_x), round(self.pacman.smooth_y))
            if smooth_cell in self.dots_grid:
                dot = self.dots_grid.pop(smooth_cell)
                dot.remove_from_sprite_lists()

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.drag_x += dx
        self.drag_y += dy

    def on_draw(self):
        self.clear()

        if self.wall_lines:
            arcade.draw_lines(self.wall_lines, (33, 33, 255), self.wall_thickness)

        self.dots.draw()

        for (c, r) in self.forty_two_coords:
            real_x, real_y = self.cc(c, r)
            sqr = arcade.rect.XYWH(
                real_x,
                real_y,
                self.cell_size * 0.5,
                self.cell_size * 0.5,
            )
            arcade.draw_rect_filled(sqr, arcade.color.PALE_ROBIN_EGG_BLUE)

        self.pacman.draw(self)
        for ghost in self.ghosts:
            ghost.draw()

        if self.pause:
            cx = self.width / 2
            cy = self.height / 2
            shade = arcade.rect.XYWH(cx, cy, self.width, self.height)
            arcade.draw_rect_filled(shade, (10, 10, 10, 170))
            if self.state == 1:
                self.died_text.draw()
            if self.state == 2:
                self.pause_text.draw()
            if self.state == 3:
                self.won_text.draw()
