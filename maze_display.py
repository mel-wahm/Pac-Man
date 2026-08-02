from mazegenerator import MazeGenerator
from game_logic import neighbor_coordinates
import arcade
from math import sin

height = 9
width = 21

maze = MazeGenerator(size=(width, height)).maze


class Pacman:
    def __init__(self, maze):
        self.x = (len(maze[0]) - 1) // 2
        self.y = (len(maze) - 1) // 2
        self.angle = 0
        self.xeye = 1
        self.yeye = 1
        self.path = {(self.x, self.y)}

    @property
    def neighbors(self):
        return neighbor_coordinates(self.x, self.y, maze)


class Ghost:
    def __init__(self, maze, renderer):
        self.x, self.y = renderer.center_coordinates(0, 0)
        self.color = arcade.color.WHITE
        self.renderer = renderer

    @property
    def draw(self):
        self.renderer.draw_monster(self.x, self.y, self.color)


class Render(arcade.Window):
    def __init__(self, maze: list,
                 pacman: Pacman
                 ghost: Ghost):
        super().__init__(1980, 1080, "PACMAN", True, True, vsync=True)
        self.background_color = (15, 15, 25)
        self.maze = maze
        self.pacman = pacman
        self.total_w = (len(self.maze[0]) - 1) / 2
        self.total_h = (len(self.maze) - 1) / 2
        self.drag_x = 0
        self.drag_y = 0
        self.cols = len(self.maze[0])
        self.rows = len(self.maze)
        self.progress = 0
        self.cell_size = min(
            (self.width - 100) / self.cols, (self.height - 100) / self.rows
        )
        self.corners = {
            (0, 0),
            (self.cols - 1, 0),
            (0, self.rows - 1),
            (self.cols - 1, self.rows - 1),
        }
        self.forty_two_coords = set()
        if self.rows >= 10 and self.cols >= 14:
            posx = (self.cols - 7) // 2
            posy = (self.rows - 5) // 2
            self.forty_two_coords = {
                (posx + 0, posy + 0),
                (posx + 4, posy + 0),
                (posx + 5, posy + 0),
                (posx + 6, posy + 0),
                (posx + 0, posy + 1),
                (posx + 6, posy + 1),
                (posx + 0, posy + 2),
                (posx + 1, posy + 2),
                (posx + 2, posy + 2),
                (posx + 4, posy + 2),
                (posx + 5, posy + 2),
                (posx + 6, posy + 2),
                (posx + 2, posy + 3),
                (posx + 4, posy + 3),
                (posx + 2, posy + 4),
                (posx + 4, posy + 4),
                (posx + 5, posy + 4),
                (posx + 6, posy + 4),
            }

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.LEFT:
            if not self.maze[self.pacman.y][self.pacman.x] & 8:
                self.pacman.x = max(self.pacman.x - 1, 0)
            self.pacman.angle = 180
            self.pacman.xeye = -1
            self.pacman.yeye = 1
        if symbol == arcade.key.RIGHT:
            if not self.maze[self.pacman.y][self.pacman.x] & 2:
                self.pacman.x = min(self.pacman.x + 1, self.cols - 1)
            self.pacman.angle = 0
            self.pacman.xeye = 1
            self.pacman.yeye = 1
        if symbol == arcade.key.UP:
            if not self.maze[self.pacman.y][self.pacman.x] & 1:
                self.pacman.y = max(self.pacman.y - 1, 0)
            self.pacman.angle = 90
            self.pacman.xeye = 1
            self.pacman.yeye = -1
        if symbol == arcade.key.DOWN:
            if not self.maze[self.pacman.y][self.pacman.x] & 4:
                self.pacman.y = min(self.pacman.y + 1, self.rows - 1)
            self.pacman.angle = 270
            self.pacman.xeye = -1
            self.pacman.yeye = 1
        self.pacman.path.add((self.pacman.x, self.pacman.y))
        if symbol == arcade.key.F:
            self.set_fullscreen(not self.fullscreen)
        if symbol == arcade.key.Q:
            exit(0)

    def center_coordinates(self, x, y):
        nx = self.width / 2 + (x - self.total_w) * self.cell_size
        ny = self.height / 2 - (y - self.total_h) * self.cell_size
        return (nx, ny)

    def on_update(self, delta_time):
        self.progress += 6 * delta_time

    def draw_pacman(self):
        cx, cy = self.center_coordinates(self.pacman.x, self.pacman.y)
        arcade.draw_arc_filled(
            cx,
            cy,
            15 * 0.025 * self.cell_size,
            15 * 0.025 * self.cell_size,
            arcade.color.YELLOW,
            30 + self.pacman.angle + 15 * sin(self.progress),
            330 + self.pacman.angle - 15 * sin(self.progress),
        )
        """arcade.draw_circle_filled(
            cx + 2 * self.pacman.xeye,
            cy + 15 * self.pacman.yeye,
            1 * 0.025 * self.cell_size,
            arcade.color.BLACK,
            num_segments=100,
        )"""

    def draw_monster(self, cx, cy, color):
        s = 0.002 * self.cell_size
        arcade.draw_arc_filled(
            cx, cy + 15 * s, 240 * s, 240 * s, color, 0, 180
        )
        rect = arcade.rect.XYWH(cx, cy - 30 * s, 240 * s, 90 * s)
        arcade.draw_rect_filled(rect, color)
        arcade.draw_arc_filled(
            cx, cy - 75 * s, 80 * s, 80 * s, color, 180, 360
        )
        arcade.draw_arc_filled(
            cx - 80 * s, cy - 75 * s, 80 * s, 80 * s, color, 180, 360
        )
        arcade.draw_arc_filled(
            cx + 80 * s, cy - 75 * s, 80 * s, 80 * s, color, 180, 360
        )
        arcade.draw_circle_filled(
            cx - 35 * s,
            cy + 15 * s,
            30 * s,
            arcade.color.WHITE,
            num_segments=32,
        )
        arcade.draw_circle_filled(
            cx - 35 * s,
            cy + 15 * s,
            20 * s,
            arcade.color.BLACK,
            num_segments=32,
        )
        arcade.draw_circle_filled(
            cx - 35 * s + 5 * s * sin(self.progress),
            cy + 19 * s,
            3 * s,
            arcade.color.WHEAT,
            num_segments=32,
        )
        arcade.draw_circle_filled(
            cx + 35 * s,
            cy + 15 * s,
            30 * s,
            arcade.color.WHITE,
            num_segments=32,
        )
        arcade.draw_circle_filled(
            cx + 35 * s,
            cy + 15 * s,
            20 * s,
            arcade.color.BLACK,
            num_segments=32,
        )
        arcade.draw_circle_filled(
            cx + 35 * s + 5 * s * sin(self.progress),
            cy + 19 * s,
            3 * s,
            arcade.color.WHEAT,
            num_segments=32,
        )

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.drag_x += dx
        self.drag_y += dy

    def on_draw(self):
        self.clear()
        wall_thickness = max(1, int(self.cell_size * 0.05))
        dot_radius = max(1, self.cell_size * 0.05)
        for r in range(len(maze)):
            for c in range(len(maze[r])):
                sx, sy = self.center_coordinates(c, r)
                half = self.cell_size / 2
                cell_val = maze[r][c]
                if cell_val & 1:
                    arcade.draw_line(
                        sx - half,
                        sy + half,
                        sx + half,
                        sy + half,
                        arcade.color.DARK_BLUE,
                        wall_thickness,
                    )
                if cell_val & 2:
                    arcade.draw_line(
                        sx + half,
                        sy + half,
                        sx + half,
                        sy - half,
                        arcade.color.DARK_BLUE,
                        wall_thickness,
                    )
                if cell_val & 4:
                    arcade.draw_line(
                        sx - half,
                        sy - half,
                        sx + half,
                        sy - half,
                        arcade.color.DARK_BLUE,
                        wall_thickness,
                    )
                if cell_val & 8:
                    arcade.draw_line(
                        sx - half,
                        sy + half,
                        sx - half,
                        sy - half,
                        arcade.color.DARK_BLUE,
                        wall_thickness,
                    )
                if (c, r) in self.forty_two_coords:
                    sqr = arcade.rect.XYWH(
                        sx,
                        sy,
                        self.cell_size * 0.5,
                        self.cell_size * 0.5,
                    )
                    arcade.draw_rect_filled(sqr, arcade.color.RED)

                elif (c, r) in self.pacman.neighbors:
                    arcade.draw_circle_filled(
                        sx,
                        sy,
                        dot_radius * 1.5,
                        arcade.color.RED,
                        num_segments=32,
                    )
                elif (c, r) not in self.pacman.path:
                    if (c, r) in self.corners:
                        arcade.draw_circle_filled(
                            sx,
                            sy,
                            dot_radius * 2.5,
                            arcade.color.WHITE,
                            num_segments=32,
                        )
                    else:
                        arcade.draw_circle_filled(
                            sx,
                            sy,
                            dot_radius,
                            arcade.color.WHITE,
                            num_segments=32,
                        )

                if c == self.pacman.x and r == self.pacman.y:
                    self.draw_pacman()
                elif c == 0 and r == 0:
                    self.draw_monster(sx, sy, arcade.color.YELLOW)
                elif c == 0 and r == self.rows - 1:
                    self.draw_monster(sx, sy, arcade.color.GREEN)
                elif c == self.cols - 1 and r == 0:
                    self.draw_monster(sx, sy, arcade.color.PURPLE)
                elif c == self.cols - 1 and r == self.rows - 1:
                    self.draw_monster(sx, sy, arcade.color.ORANGE)


pacman = Pacman(maze)
Render(maze, pacman)
ghost = Ghost(maze)
arcade.run()
