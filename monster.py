import arcade
from math import sin

class	Monster(arcade.Window):
	def __init__(self):
		super().__init__(1980, 1080, "GHOST", True)
		self.progress = 0
		self.background_color = (15, 15, 25)

	def on_update(self, delta_time):
		self.progress += 6 * delta_time

	def on_key_press(self, symbol, modifiers):
		if symbol == arcade.key.Q:
			exit(1)
	def draw_monster(self, cx, cy):
		arcade.draw_arc_filled(cx, cy + 60, 240, 240, arcade.color.RED,
								 0, 180)
		rect = arcade.rect.XYWH(cx, cy - 15, 240, 150)
		arcade.draw_rect_filled(rect, arcade.color.RED)
		arcade.draw_arc_filled(cx, cy - 85, 80, 80, arcade.color.RED,
								 180, 360)
		arcade.draw_arc_filled(cx - 80, cy - 85, 80, 80, arcade.color.RED,
										 180, 360)
		arcade.draw_arc_filled(cx + 80, cy - 85, 80, 80, arcade.color.RED,
												 180, 360)
		arcade.draw_circle_filled(cx - 35, cy + 50, 30, arcade.color.WHITE, num_segments=150)	
		arcade.draw_circle_filled(cx - 35, cy + 50, 20, arcade.color.BLACK, num_segments=150)	
		arcade.draw_circle_filled(cx - 35 + 5 * sin(self.progress), cy + 54, 3, arcade.color.WHEAT, num_segments=150)	
		arcade.draw_circle_filled(cx + 35, cy + 50, 30, arcade.color.WHITE, num_segments=150)	
		arcade.draw_circle_filled(cx + 35, cy + 50, 20, arcade.color.BLACK, num_segments=150)	
		arcade.draw_circle_filled(cx + 35 + 5 * sin(self.progress), cy + 54, 3, arcade.color.WHEAT, num_segments=150)	
		
	def	on_draw(self):
		self.clear()
		cx, cy = self.width / 2, self.height / 2
		self.draw_monster(cx, cy)
		
Monster()
arcade.run()