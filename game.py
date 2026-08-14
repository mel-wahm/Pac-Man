from math import hypot
import arcade
import config
from random import sample
from game_logic import center_coordinates
from ghost import Ghost
from pacman import Directions, Pacman
from ingame_settings import InGameSettings

class Game(arcade.View):
	def __init__(self, maze: list, screen_view):
		super().__init__()

		self.screen_view = screen_view
		self.super_gum_textures = [
			arcade.load_texture("fruits/super_fruit_yellow.png"),
			arcade.load_texture("fruits/super_fruit_pink.png"),
			arcade.load_texture("fruits/super_fruit_cyan.png"),
			arcade.load_texture("fruits/super_fruit_green.png"),
		]
		maze[0][len(maze[0]) // 2] -= 1
		maze[len(maze) - 1][len(maze[0]) // 2] -= 4
		maze[len(maze) // 2][0] -= 8
		maze[len(maze) // 2][len(maze[0]) - 1] -= 2
		self.background_color = (20, 20, 30)
		self.intro = 1
		self.pac_gums = 1000
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
		self.win_timer = 0.0
		arcade.load_font("fonts/Renogare-Regular.otf")
		cx = self.width / 2
		cy = self.height / 2
		
		self.pause_text = arcade.Text(
			"PAUSE",
			cx,
			cy,
			(200, 200, 200),
			font_size=160,
			anchor_x="center",
			anchor_y="center",
			font_name="Renogare",
			# bold=True,
		)
		self.died_text = arcade.Text(
			"YOU DIED",
			cx,
			cy,
			(180, 15, 15),
			font_size=80,
			anchor_x="center",
			anchor_y="center",
			font_name="Renogare",
		)
		self.won_text = arcade.Text(
			"YOU WON",
			cx,
			cy,
			(255, 200, 0),
			font_size=280,
			anchor_x="center",
			anchor_y="center",
			font_name="Renogare",
			# bold=True,
		)
		sidebar_width = 170
		padding = 20
		available_w = self.width - sidebar_width - padding
		available_h = self.height - padding
		self.cell_size = min(available_w / self.cols, available_h / self.rows)
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
		self.all_cords = []
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
					self.all_cords.append((c, r))
		self.drawing_dots = sample(
			self.all_cords, min(len(self.all_cords), self.pac_gums)
		)
		for cell in self.drawing_dots:
			c, r = cell
			real_x, real_y = self.center(c, r)
			dot_r = int(self.cell_size * 0.05)
			dot = arcade.SpriteCircle(
				radius=max(1, dot_r), color=(255, 255, 0)
			)
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
		self.sec = 0
		self.progress = 0
		self.ghost_speed = 0
		self.pacman_speed = 0

		self.pacman.reset_game()
		self.won_text.font_size = 280
		self.win_timer = 0.0
		
		for g in self.ghosts:
			g.reset_game()

		self.dots = arcade.SpriteList()
		self.dots_grid = {}
		self.drawing_dots = sample(
			self.all_cords, min(len(self.all_cords), self.pac_gums)
		)
		for cell in self.drawing_dots:
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

	def on_key_press(self, symbol, modifiers):
		if symbol == arcade.key.C and modifiers & arcade.key.MOD_CTRL:
			exit()
		if symbol == config.keys["UP"]:
			self.pacman.set_next_direction(Directions.UP)
		if symbol == config.keys["DOWN"]:
			self.pacman.set_next_direction(Directions.DOWN)
		if symbol == config.keys["RIGHT"]:
			self.pacman.set_next_direction(Directions.RIGHT)
		if symbol == config.keys["LEFT"]:
			self.pacman.set_next_direction(Directions.LEFT)
		if symbol == arcade.key.ESCAPE:
			set_view = InGameSettings(self, self.screen_view)
			self.window.show_view(set_view)
		if symbol == arcade.key.SPACE:
			self.state = 2
			self.pause = not (self.pause)


	def center(self, x, y):
		sidebar_width = 170
		padding = 20
		center_x = sidebar_width + (self.width - sidebar_width - padding) / 2
		center_y = self.height / 2

		nx = center_x + (x - self.total_w) * self.cell_size
		ny = center_y - (y - self.total_h) * self.cell_size
		return (nx, ny)

	def on_update(self, delta_time):
		gst_speed = 8
		pcmn_speed = 0.12
		if len(self.dots) == 0:
			self.pause = 1
			self.state = 3

		if self.state == 3:
			self.win_timer = min(1.0, self.win_timer + delta_time * 2.0)
			t = self.win_timer
			ease_out = t * (2 - t)
			self.won_text.font_size = int(280 - (280 - 60) * ease_out)
		for ghost in self.ghosts:
			if (
				hypot(
					(ghost.smooth_x - self.pacman.smooth_x),
					(ghost.smooth_y - self.pacman.smooth_y),
				)
				< 0.5
			):
				if not ghost.edible:
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
						g.edible_timer = 0
						g.edible = 0
						g.r_c = g.default
						g.path = []
						g.smooth_x = float(g.default[0])
						g.smooth_y = float(g.default[1])
						g.draw_cords = self.center(g.smooth_x, g.smooth_y)
						g.ghost_freeze = 1
					if self.pacman.death == 3:
						self.reset_game()
						self.state = 1
						self.pause = 1
						self.pacman.death = 0
						self.pacman.path = {(self.pacman.x, self.pacman.y)}
					break
				else:
					self.pacman.score += 100
					self.pacman.score_text.text = f"SCORE: {self.pacman.score}"
					ghost.r_c = ghost.default
					ghost.smooth_x, ghost.smooth_y = ghost.default
					ghost.draw_cords = self.center(ghost.smooth_x, ghost.smooth_y)
					ghost.ghost_freeze = 5
					ghost.edible_timer = 0
					ghost.edible = 0
					break

		if not self.pause:
			self.sec += delta_time
			self.progress += 6 * delta_time
			self.ghost_speed += delta_time
			self.pacman_speed += delta_time

			should_choose_target = False
			if self.ghost_speed > 2.5 / gst_speed:
				self.ghost_speed = 0
				should_choose_target = True

			for ghost in self.ghosts:
				ghost.ghost_freeze -= delta_time
				if ghost.ghost_freeze <= 0:
					if should_choose_target:
						ghost.choose_target(self.pacman)
					ghost.update(gst_speed, delta_time)
					ghost.draw_cords = self.center(ghost.smooth_x, ghost.smooth_y)

			if self.pacman_speed > pcmn_speed:
				self.pacman_speed = 0
				self.pacman.update()
			if not self.pacman.teleport:
				self.pacman.smooth_animation(delta_time, pcmn_speed)

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
						ghost.edible_timer = 20
				dot.remove_from_sprite_lists()

	def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
		self.drag_x += dx
		self.drag_y += dy

	def on_draw(self):
		self.clear()
		if self.wall_lines:
			arcade.draw_lines(
				self.wall_lines, (33, 33, 255), self.wall_thickness
			)

		self.dots.draw()

		for c, r in self.forty_two_coords:
			real_x, real_y = self.center(c, r)
			sqr = arcade.rect.XYWH(
				real_x,
				real_y,
				self.cell_size * 0.5,
				self.cell_size * 0.5,
			)
			arcade.draw_rect_filled(sqr, (33, 33, 255))

		self.pacman.draw(self)
		for ghost in self.ghosts:
			ghost.draw()

		sidebar_x = 20

		self.pacman.score_text.x = sidebar_x
		self.pacman.score_text.y = self.height - 100
		self.pacman.score_text.draw()
		self.pacman.lives_text.x = sidebar_x
		self.pacman.lives_text.y = self.height - 170
		self.pacman.lives_text.draw()

		lives_remaining = 3 - self.pacman.death
		for i in range(lives_remaining):
			arcade.draw_arc_filled(
				sidebar_x + 20 + (i * 45),
				self.height - 230,
				32,
				32,
				arcade.color.YELLOW,
				30,
				330,
			)
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
