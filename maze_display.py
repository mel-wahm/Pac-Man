from mazegenerator import MazeGenerator
from game_logic import neighbor_coordinates, center_coordinates
import arcade
from math import sin
import random
from enum import Enum

height = 13
width = 23

maze = MazeGenerator(size=(width, height)).maze


class Directions(Enum):
	LEFT = "left"
	RIGHT = "right"
	UP = "up"
	DOWN = "down"


class Pacman:
	def __init__(self, maze):
		self.x = (len(maze[0]) - 1) // 2
		self.y = (len(maze) - 1) // 2
		self.angle = 0
		self.path = {(self.x, self.y)}
		self.direction = Directions.DOWN
		self.next_direction = Directions.DOWN

	def can_turn(self, x, y, direction, maze):
		if direction == Directions.UP:
			return not (maze[y][x] & 1)
		if direction == Directions.RIGHT:
			return not (maze[y][x] & 2)
		if direction == Directions.DOWN:
			return not (maze[y][x] & 4)
		if direction == Directions.LEFT:
			return not (maze[y][x] & 8)
		return False

	@property
	def neighbors(self):
		return neighbor_coordinates(self.x, self.y, maze)

	def draw(self, renderer):
		cx, cy = renderer.center_coordinates(self.x, self.y)
		arcade.draw_arc_filled(
			cx,
			cy,
			15 * 0.025 * renderer.cell_size,
			15 * 0.025 * renderer.cell_size,
			arcade.color.YELLOW,
			30 + self.angle + 15 * sin(renderer.progress),
			330 + self.angle - 15 * sin(renderer.progress),
		)


class Ghost:
	def __init__(self, real_cords, draw_cords, color, c_size):
		self.c_size = c_size
		self.color = color
		self.real_cords = real_cords
		self.draw_cords = draw_cords

	def draw_monster(self):
		cx, cy = self.draw_cords
		s = 0.002 * self.c_size
		arcade.draw_arc_filled(cx, cy + 15 * s, 240 * s, 240 * s, self.color, 0, 180)
		rect = arcade.rect.XYWH(cx, cy - 30 * s, 240 * s, 90 * s)
		arcade.draw_rect_filled(rect, self.color)
		arcade.draw_arc_filled(cx, cy - 75 * s, 80 * s, 80 * s, self.color, 180, 360)
		arcade.draw_arc_filled(
			cx - 80 * s, cy - 75 * s, 80 * s, 80 * s, self.color, 180, 360
		)
		arcade.draw_arc_filled(
			cx + 80 * s, cy - 75 * s, 80 * s, 80 * s, self.color, 180, 360
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
			cx - 35 * s,
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
			cx + 35 * s,
			cy + 19 * s,
			3 * s,
			arcade.color.WHEAT,
			num_segments=32,
		)


class Render(arcade.Window):
	def __init__(self, maze: list):
		super().__init__(1980, 1080, "PACMAN", True, True, vsync=True)
		self.background_color = (15, 15, 25)
		self.maze = maze
		self.pacman = Pacman(maze)
		self.total_w = (len(self.maze[0]) - 1) / 2
		self.total_h = (len(self.maze) - 1) / 2
		self.drag_x = 0
		self.drag_y = 0
		self.cols = len(self.maze[0])
		self.rows = len(self.maze)
		self.progress = 0
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
				self.center_coordinates(0, 0),
				arcade.color.GREEN,
				self.cell_size,
			),
			Ghost(
				(self.cols - 1, 0),
				self.center_coordinates(self.cols - 1, 0),
				arcade.color.PURPLE,
				self.cell_size,
			),
			Ghost(
				(0, self.rows - 1),
				self.center_coordinates(0, self.rows - 1),
				arcade.color.ORANGE,
				self.cell_size,
			),
			Ghost(
				(self.cols - 1, self.rows - 1),
				self.center_coordinates(self.cols - 1, self.rows - 1),
				arcade.color.YELLOW,
				self.cell_size,
			),
		}
		self.forty_two_coords = set()
		if self.rows >= 10 and self.cols >= 14:
			poreal_x = (self.cols - 7) // 2
			poreal_y = (self.rows - 5) // 2
			self.forty_two_coords = {
				(poreal_x + 0, poreal_y + 0),
				(poreal_x + 4, poreal_y + 0),
				(poreal_x + 5, poreal_y + 0),
				(poreal_x + 6, poreal_y + 0),
				(poreal_x + 0, poreal_y + 1),
				(poreal_x + 6, poreal_y + 1),
				(poreal_x + 0, poreal_y + 2),
				(poreal_x + 1, poreal_y + 2),
				(poreal_x + 2, poreal_y + 2),
				(poreal_x + 4, poreal_y + 2),
				(poreal_x + 5, poreal_y + 2),
				(poreal_x + 6, poreal_y + 2),
				(poreal_x + 2, poreal_y + 3),
				(poreal_x + 4, poreal_y + 3),
				(poreal_x + 2, poreal_y + 4),
				(poreal_x + 4, poreal_y + 4),
				(poreal_x + 5, poreal_y + 4),
				(poreal_x + 6, poreal_y + 4),
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

	def center_coordinates(self, x, y):
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
		self.progress += 6 * delta_time
		self.ghost_speed += delta_time
		self.pacman_speed += delta_time
		if self.ghost_speed > 0.5:
			# self.seconds += 1
			self.ghost_speed = 0
			for ghost in self.ghosts:
				ghost.real_cords = random.choice(
					neighbor_coordinates(
						ghost.real_cords[0], ghost.real_cords[1], self.maze
					)
				)
				ghost.draw_cords = self.center_coordinates(
					ghost.real_cords[0], ghost.real_cords[1]
				)
		if self.pacman_speed > 0.15:
			self.pacman.path.add((self.pacman.x, self.pacman.y))
			self.pacman_speed = 0
			if self.pacman.can_turn(self.pacman.x, self.pacman.y,
						   self.pacman.next_direction, maze):
				self.pacman.direction = self.pacman.next_direction
			if self.pacman.direction == Directions.LEFT:
				if not self.maze[self.pacman.y][self.pacman.x] & 8:
					self.pacman.x = max(self.pacman.x - 1, 0)
				self.pacman.angle = 180
			if self.pacman.direction == Directions.RIGHT:
				if not self.maze[self.pacman.y][self.pacman.x] & 2:
					self.pacman.x = min(self.pacman.x + 1, self.cols - 1)
				self.pacman.angle = 0
			if self.pacman.direction == Directions.UP:
				if not self.maze[self.pacman.y][self.pacman.x] & 1:
					self.pacman.y = max(self.pacman.y - 1, 0)
				self.pacman.angle = 90
			if self.pacman.direction == Directions.DOWN:
				if not self.maze[self.pacman.y][self.pacman.x] & 4:
					self.pacman.y = min(self.pacman.y + 1, self.rows - 1)
				self.pacman.angle = 270

	def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
		self.drag_x += dx
		self.drag_y += dy

	def on_draw(self):
		self.clear()
		wall_thickness = max(1, int(self.cell_size * 0.05))
		dot_radius = max(1, self.cell_size * 0.05)
		# pacman_neighbors = self.pacman.neighbors
		for r in range(len(maze)):
			for c in range(len(maze[r])):
				real_x, real_y = self.center_coordinates(c, r)
				half = self.cell_size / 2
				cell_val = maze[r][c]
				if cell_val & 1:
					arcade.draw_line(
						real_x - half,
						real_y + half,
						real_x + half,
						real_y + half,
						arcade.color.DARK_BLUE,
						wall_thickness,
					)
				if cell_val & 2:
					arcade.draw_line(
						real_x + half,
						real_y + half,
						real_x + half,
						real_y - half,
						arcade.color.DARK_BLUE,
						wall_thickness,
					)
				if cell_val & 4:
					arcade.draw_line(
						real_x - half,
						real_y - half,
						real_x + half,
						real_y - half,
						arcade.color.DARK_BLUE,
						wall_thickness,
					)
				if cell_val & 8:
					arcade.draw_line(
						real_x - half,
						real_y + half,
						real_x - half,
						real_y - half,
						arcade.color.DARK_BLUE,
						wall_thickness,
					)
				if (c, r) in self.forty_two_coords:
					sqr = arcade.rect.XYWH(
						real_x,
						real_y,
						self.cell_size * 0.5,
						self.cell_size * 0.5,
					)
					arcade.draw_rect_filled(sqr, arcade.color.AIR_SUPERIORITY_BLUE)

				elif (c, r) not in self.pacman.path:
					if (c, r) in self.corners:
						arcade.draw_circle_filled(
							real_x,
							real_y,
							dot_radius * 2.5,
							arcade.color.WHITE,
							num_segments=32,
						)
					else:
						arcade.draw_circle_filled(
							real_x,
							real_y,
							dot_radius,
							arcade.color.WHITE,
							num_segments=32,
						)

				# if c == self.pacman.x and r == self.pacman.y:
		self.pacman.draw(self)
		for ghost in self.ghosts:
			ghost.draw_monster()


Render(maze)
arcade.run()
