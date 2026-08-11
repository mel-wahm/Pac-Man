import arcade
from game import Game
from menu import Selection, Menu
from key_bindings import Control

class   Settings(arcade.View):
	def __init__(self, previous_view, game_view):
		super().__init__()
		self.settings_wallpaper = arcade.load_texture("photos/settings.png")
		self.previous_view = previous_view
		self.game_view = game_view
		self.cx, self.cy = self.width / 2, self.height / 2
		self._return = Selection("Return", lambda: self.returning())
		self._controls = Selection("Controls", lambda: self.controls())
		self.menus = Menu([self._controls, self._return], self.width / 2, self.height / 2)

	def returning(self):
		self.window.show_view(self.previous_view)
	def controls(self):
		control_view = Control(self)
		self.window.show_view(control_view)

	def on_key_press(self, symbol, modifiers):
		if symbol == arcade.key.UP:
			self.menus.move_up()
		if symbol == arcade.key.DOWN:
			self.menus.move_down()
		if symbol == arcade.key.ENTER:
			self.menus.action()
		if symbol == arcade.key.ESCAPE:
			self.window.show_view(self.previous_view)

	def on_draw(self):
		self.clear()
		cx = self.window.width
		cy = self.window.height
		r = arcade.rect.XYWH(self.cx, self.cy, cx, cy)
		arcade.draw_texture_rect(self.settings_wallpaper, r)
		self.menus.draw_texts()
