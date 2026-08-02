from mazegenerator import MazeGenerator
import arcade
from math import sin

height = 9
width = 9

maze = MazeGenerator(size=(width,height)).maze

class Render(arcade.Window):
	def __init__(self, maze: list):
		super().__init__(1980, 1080,
				   'PACMAN', True, True, vsync=True)
		self.background_color = (15, 15, 25)
		self.maze = maze
		self.total_w = (len(self.maze[0]) - 1) / 2
		self.total_h = (len(self.maze) - 1) / 2
		self.drag_x = 0
		self.drag_y = 0
		self.cols = len(self.maze[0])
		self.rows = len(self.maze)
		self.progress = 0
		self.cell_size = 800 / max(self.cols, self.rows)

	def on_key_press(self, symbol, modifiers):
		if symbol == arcade.key.Q:
			exit(1)

	def center_coordinates(self, x, y):
		middle_collumn = (len(self.maze[0]) - 1) / 2 
		middle_row = (len(self.maze) - 1) / 2
		nx = self.width / 2 + (x - middle_collumn) * self.cell_size
		ny = self.height / 2 - (y - middle_row) * self.cell_size
		return (nx, ny)

	def on_update(self, delta_time):
		self.progress += 6 * delta_time

	def	get_lines(self, cords: tuple[int, int]):
		x, y = cords
		s = self.cell_size
		half = s / 2
		center_x, center_y = self.center_coordinates(x, y)
		return {
			1: [(center_x - half, center_y + half), (center_x + half, center_y + half)],
			2: [(center_x + half, center_y + half), (center_x + half, center_y - half)],
			4: [(center_x - half, center_y - half), (center_x + half, center_y - half)],
			8: [(center_x - half, center_y + half), (center_x - half, center_y - half)],
		}

	def draw_pacman(self, cx, cy):
		arcade.draw_arc_filled(cx, cy, 15 * 0.025 * self.cell_size,
						 15 * 0.025 * self.cell_size, arcade.color.YELLOW,
						 30 + 15 * sin(self.progress),
						 330 - 15 * sin(self.progress))
		arcade.draw_circle_filled(cx + 1 * 0.025 * self.cell_size - (1 * sin(self.progress)),
							cy + 5 * 0.025 * self.cell_size + (1 * sin(self.progress)),
							1 * 0.025 * self.cell_size, arcade.color.BLACK, num_segments=100)

	def draw_monster(self, cx, cy, color):
		s = 0.002 * self.cell_size
		arcade.draw_arc_filled(cx, cy + 15 * s, 240 * s, 240 * s, color, 0, 180)
		rect = arcade.rect.XYWH(cx, cy - 30 * s, 240 * s, 90 * s)
		arcade.draw_rect_filled(rect, color)
		arcade.draw_arc_filled(cx, cy - 75 * s, 80 * s, 80 * s, color, 180, 360)
		arcade.draw_arc_filled(cx - 80 * s, cy - 75 * s, 80 * s, 80 * s, color, 180, 360)
		arcade.draw_arc_filled(cx + 80 * s, cy - 75 * s, 80 * s, 80 * s, color, 180, 360)
		arcade.draw_circle_filled(cx - 35 * s, cy + 15 * s, 30 * s, arcade.color.WHITE, num_segments=150)
		arcade.draw_circle_filled(cx - 35 * s, cy + 15 * s, 20 * s, arcade.color.BLACK, num_segments=150)
		arcade.draw_circle_filled(cx - 35 * s + 5 * s * sin(self.progress), cy + 19 * s, 3 * s, arcade.color.WHEAT, num_segments=150)
		arcade.draw_circle_filled(cx + 35 * s, cy + 15 * s, 30 * s, arcade.color.WHITE, num_segments=150)
		arcade.draw_circle_filled(cx + 35 * s, cy + 15 * s, 20 * s, arcade.color.BLACK, num_segments=150)
		arcade.draw_circle_filled(cx + 35 * s + 5 * s * sin(self.progress), cy + 19 * s, 3 * s, arcade.color.WHEAT, num_segments=150)

	def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
		self.drag_x += dx
		self.drag_y += dy

	def on_draw(self):
		self.clear()
		
		for r in range(len(maze)):
			for c in range(len(maze[r])):
				lines = self.get_lines((c, r))
				for flag, square in lines.items():
					x, y = square
					if maze[r][c] & flag:
						arcade.draw_line(x[0], x[1], y[0], y[1], arcade.color.DARK_BLUE, 5)
					sx, sy = self.center_coordinates(c, r)
					if c == (self.cols - 1) // 2 and r == (self.rows - 1) // 2:
						self.draw_pacman(sx, sy)
					elif c == 0 and r == 0:
						self.draw_monster(sx, sy, arcade.color.YELLOW)
					elif c == 0 and r == self.rows - 1:
						self.draw_monster(sx, sy, arcade.color.GREEN)
					elif c == self.cols - 1 and r == 0:
						self.draw_monster(sx, sy, arcade.color.PURPLE)
					elif c == self.cols - 1 and r == self.rows - 1:
						self.draw_monster(sx, sy, arcade.color.ORANGE)
					else:
						arcade.draw_circle_filled(sx, sy, 2, arcade.color.WHITE)

Render(maze)
arcade.run()

