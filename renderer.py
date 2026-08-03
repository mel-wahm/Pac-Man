import arcade

from game_logic import center_coordinates
from ghost import Ghost
from pacman import Directions, Pacman


class Render(arcade.Window):
    def __init__(self, maze: list):
        super().__init__(1980, 1080, "PACMAN", True, True, vsync=True)
        self.background_color = (10, 10, 30)
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
        self.cell_size = min(
            (self.width - 100) / self.cols, (self.height - 100) / self.rows
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

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.LEFT:
            self.pacman.next_direction = Directions.LEFT
        if symbol == arcade.key.RIGHT:
            self.pacman.next_direction = Directions.RIGHT
        if symbol == arcade.key.UP:
            self.pacman.next_direction = Directions.UP
        if symbol == arcade.key.DOWN:
            self.pacman.next_direction = Directions.DOWN
        if symbol == arcade.key.F:
            self.set_fullscreen(not self.fullscreen)
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
        self.sec += delta_time
        self.progress += 6 * delta_time
        self.ghost_speed += delta_time
        self.pacman_speed += delta_time


        if self.ghost_speed > 0.45:
            self.ghost_speed = 0
            for ghost in self.ghosts:
                ghost.choose_target()

        for ghost in self.ghosts:
            ghost.update(7, delta_time)
            ghost.draw_cords = self.cc(ghost.smooth_x, ghost.smooth_y)

        if self.pacman_speed > 0.15:
            self.pacman_speed = 0
            self.pacman.update()
        self.pacman.smooth_animation(28, delta_time)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.drag_x += dx
        self.drag_y += dy

    def on_draw(self):
        self.clear()
        wall_thickness = max(1, int(self.cell_size * 0.05))
        dot_radius = max(1, self.cell_size * 0.05)
        for r in range(len(self.maze)):
            for c in range(len(self.maze[r])):
                real_x, real_y = self.cc(c, r)
                half = self.cell_size / 2
                cell_val = self.maze[r][c]
                if cell_val & 1:
                    arcade.draw_line(
                        real_x - half,
                        real_y + half,
                        real_x + half,
                        real_y + half,
                        (33, 33, 255),
                        wall_thickness * 2,
                    )
                if cell_val & 2:
                    arcade.draw_line(
                        real_x + half,
                        real_y + half,
                        real_x + half,
                        real_y - half,
                        (33, 33, 255),
                        wall_thickness * 2,
                    )

                if cell_val & 4:
                    arcade.draw_line(
                        real_x - half,
                        real_y - half,
                        real_x + half,
                        real_y - half,
                        (33, 33, 255),
                        wall_thickness * 2,
                    )

                if cell_val & 8:
                    arcade.draw_line(
                        real_x - half,
                        real_y + half,
                        real_x - half,
                        real_y - half,
                        (33, 33, 255),
                        wall_thickness * 2,
                    )

                if (c, r) in self.forty_two_coords:
                    sqr = arcade.rect.XYWH(
                        real_x,
                        real_y,
                        self.cell_size * 0.5,
                        self.cell_size * 0.5,
                    )

                    arcade.draw_rect_filled(sqr, arcade.color.PALE_ROBIN_EGG_BLUE)

                elif (c, r) not in self.pacman.path:
                    if (c, r) in self.corners:
                        arcade.draw_circle_filled(
                            real_x,
                            real_y,
                            dot_radius * 2.5,
                            (255, 255, 0),
                            num_segments=32,
                        )
                    else:
                        arcade.draw_circle_filled(
                            real_x,
                            real_y,
                            dot_radius,
                            (255, 255, 0),
                            num_segments=32,
                        )

        self.pacman.draw(self)
        for ghost in self.ghosts:
            ghost.draw()
