import arcade
import math


class Arc(arcade.Window):
	def __init__(self):
		super().__init__(1980, 1080, 'Pac-Man Character', True, True)
		self.progress = 0
	def on_update(self, delta_time):
		self.progress += 6 * delta_time
	def on_key_press(self, symbol, modifiers):
		if symbol == arcade.key.Q:
			exit(1)
	def draw_pacman(self, cx, cy):
		arcade.draw_arc_filled(cx, cy, 200, 200, arcade.color.YELLOW,
								 30 + 15 * math.sin(self.progress),
								 330 - 15 * math.sin(self.progress))
		arcade.draw_circle_filled(cx + 12 - (4 * math.sin(self.progress)),
							cy + 60 + (4 * math.sin(self.progress)),
							10, arcade.color.BLACK, num_segments=100)
		arcade.draw_circle_filled(cx + 12 - (4 * math.sin(self.progress)),
									cy + 60 + (4 * math.sin(self.progress)),
									8, arcade.color.WHITE, num_segments=100)
		arcade.draw_circle_filled(cx + 12 - (4 * math.sin(self.progress)),
									cy + 60 + (4 * math.sin(self.progress)),
									5, arcade.color.BLACK, num_segments=100)
	def on_draw(self):
		self.clear()
		cx, cy = self.width / 2, self.height / 2
		self.draw_pacman(cx, cy)
Arc()
arcade.run()