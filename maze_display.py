from mazegenerator import MazeGenerator
import arcade
from math import sin

height = 13
width = 15

maze = MazeGenerator(size=(width, height)).maze


class Pacman:
    def __init__(self, maze):
        self.x = (len(maze[0]) - 1) // 2
        self.y = (len(maze) - 1) // 2
        self.angle = 0
        self.xeye = 1
        self.yeye = 1
        self.path = set()


class Render(arcade.Window):
    def __init__(self, maze: list, pacman: Pacman):
        super().__init__(1980, 1080, "PACMAN", True, True, vsync=True)
        self.background_color = (15, 15, 25)
        self.maze = maze
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
        self.forty_two_coords = []
        if self.rows >= 10 and self.cols >= 14:
            posx = (self.cols - 7) // 2
            posy = (self.rows - 5) // 2
            self.forty_two_coords = [
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
            ]

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.LEFT:
            if not self.maze[pacman.y][pacman.x] & 8:
                pacman.x = max(pacman.x - 1, 0)
            pacman.angle = 180
            pacman.xeye = -1
            pacman.yeye = 1
        if symbol == arcade.key.RIGHT:
            if not self.maze[pacman.y][pacman.x] & 2:
                pacman.x = min(pacman.x + 1, self.cols - 1)
            pacman.angle = 0
            pacman.xeye = 1
            pacman.yeye = 1
        if symbol == arcade.key.UP:
            if not self.maze[pacman.y][pacman.x] & 1:
                pacman.y = max(pacman.y - 1, 0)
            pacman.angle = 90
            pacman.xeye = 1
            pacman.yeye = -1
        if symbol == arcade.key.DOWN:
            if not self.maze[pacman.y][pacman.x] & 4:
                pacman.y = min(pacman.y + 1, self.rows - 1)
            pacman.angle = 270
            pacman.xeye = -1
            pacman.yeye = 1
        if symbol == arcade.key.F:
            self.set_fullscreen(not self.fullscreen)
        if symbol == arcade.key.Q:
            exit(0)

    def center_coordinates(self, x, y):
        middle_collumn = (len(self.maze[0]) - 1) / 2
        middle_row = (len(self.maze) - 1) / 2
        nx = self.width / 2 + (x - middle_collumn) * self.cell_size
        ny = self.height / 2 - (y - middle_row) * self.cell_size
        return (nx, ny)

    def on_update(self, delta_time):
        self.progress += 6 * delta_time

    def get_lines(self, cords: tuple[int, int]):
        x, y = cords
        s = self.cell_size
        half = s / 2
        center_x, center_y = self.center_coordinates(x, y)
        return {
            1: [
                (center_x - half, center_y + half),
                (center_x + half, center_y + half),
            ],
            2: [
                (center_x + half, center_y + half),
                (center_x + half, center_y - half),
            ],
            4: [
                (center_x - half, center_y - half),
                (center_x + half, center_y - half),
            ],
            8: [
                (center_x - half, center_y + half),
                (center_x - half, center_y - half),
            ],
        }

    def draw_pacman(self, pacman):
        cx, cy = self.center_coordinates(pacman.x, pacman.y)
        arcade.draw_arc_filled(
            cx,
            cy,
            15 * 0.025 * self.cell_size,
            15 * 0.025 * self.cell_size,
            arcade.color.YELLOW,
            30 + pacman.angle + 15 * sin(self.progress),
            330 + pacman.angle - 15 * sin(self.progress),
        )
        arcade.draw_circle_filled(
            cx + 2 * pacman.xeye,
            cy + 15 * pacman.yeye,
            1 * 0.025 * self.cell_size,
            arcade.color.BLACK,
            num_segments=100,
        )

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
            num_segments=150,
        )
        arcade.draw_circle_filled(
            cx - 35 * s,
            cy + 15 * s,
            20 * s,
            arcade.color.BLACK,
            num_segments=150,
        )
        arcade.draw_circle_filled(
            cx - 35 * s + 5 * s * sin(self.progress),
            cy + 19 * s,
            3 * s,
            arcade.color.WHEAT,
            num_segments=150,
        )
        arcade.draw_circle_filled(
            cx + 35 * s,
            cy + 15 * s,
            30 * s,
            arcade.color.WHITE,
            num_segments=150,
        )
        arcade.draw_circle_filled(
            cx + 35 * s,
            cy + 15 * s,
            20 * s,
            arcade.color.BLACK,
            num_segments=150,
        )
        arcade.draw_circle_filled(
            cx + 35 * s + 5 * s * sin(self.progress),
            cy + 19 * s,
            3 * s,
            arcade.color.WHEAT,
            num_segments=150,
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
                lines = self.get_lines((c, r))
                for flag, square in lines.items():
                    x, y = square
                    if maze[r][c] & flag:
                        arcade.draw_line(
                            x[0],
                            x[1],
                            y[0],
                            y[1],
                            arcade.color.DARK_BLUE,
                            wall_thickness,
                        )
                    sx, sy = self.center_coordinates(c, r)
                    pacman.path.add((pacman.x, pacman.y))
                    # print(pacman.path)
                    if c == pacman.x and r == pacman.y:
                        self.draw_pacman(pacman)
                    elif c == 0 and r == 0:
                        self.draw_monster(sx, sy, arcade.color.YELLOW)
                    elif c == 0 and r == self.rows - 1:
                        self.draw_monster(sx, sy, arcade.color.GREEN)
                    elif c == self.cols - 1 and r == 0:
                        self.draw_monster(sx, sy, arcade.color.PURPLE)
                    elif c == self.cols - 1 and r == self.rows - 1:
                        self.draw_monster(sx, sy, arcade.color.ORANGE)

                    if (c, r) in self.forty_two_coords:
                        sqr = arcade.rect.XYWH(
                            sx,
                            sy,
                            self.cell_size * 0.5,
                            self.cell_size * 0.5,
                        )
                        arcade.draw_rect_filled(sqr, arcade.color.RED)
                    elif (c, r) not in pacman.path:
                        arcade.draw_circle_filled(
                            sx, sy, dot_radius, arcade.color.WHITE
                        )


pacman = Pacman(maze)
# print(pacman.x, pacman.y)
# exit()
Render(maze, pacman)
arcade.run()
