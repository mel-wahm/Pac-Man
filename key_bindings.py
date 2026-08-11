import arcade
import pyglet

# from game import Game
from menu import Selection, Menu
class	Control(arcade.View):
	def __init__(self, previous_view, game):
		super().__init__()
		self.previous_view = previous_view
		self.wallpaper = arcade.load_texture("photos/settings.png")
		self.left = Selection(f"Move left:   {pyglet.window.key.symbol_string(game.keys["LEFT"])}",
					lambda: self.listen())
		self.right = Selection(f"Move right:   {pyglet.window.key.symbol_string(game.keys["RIGHT"])}",
					lambda: self.listen())
		self.up = Selection(f"Move up:   {pyglet.window.key.symbol_string(game.keys["UP"])}",
					lambda: self.listen())
		self.down = Selection(f"Move down:   {pyglet.window.key.symbol_string(game.keys["DOWN"])}",
					lambda: self.listen())
		self.menus = Menu([self.up, self.down, self.right, self.left],
					self.width / 2, self.height / 2)

	def on_key_press(self, symbol, modifiers):
		if symbol == arcade.key.UP:
			self.menus.move_up()
		if symbol == arcade.key.DOWN:
			self.menus.move_down()
		if symbol == arcade.key.ENTER:
			self.menus.action()
		if symbol == arcade.key.ESCAPE:
			self.window.show_view(self.previous_view)

	def listen(self):
		pass

	def on_draw(self):
		self.clear()
		r = arcade.rect.XYWH(self.width / 2, self.height / 2, self.width, self.height)
		arcade.draw_texture_rect(self.wallpaper, r)
		r = arcade.rect.XYWH(self.width / 2, self.height / 2, self.width, self.height)
		arcade.draw_rect_filled(r, (0, 0, 0, 220))
		self.menus.draw_texts()
	