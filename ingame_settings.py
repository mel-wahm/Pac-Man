import arcade
import config
from menu import Selection, Menu
from mazegenerator import MazeGenerator

class InGameSettings(arcade.View):
	def __init__(self, game_view, screen_view):
		super().__init__()
		self.settings_wallpaper = arcade.load_texture("photos/settings.png")
		arcade.load_font("fonts/Renogare-Regular.otf")
		
		self.game_view = game_view
		self.screen_view = screen_view

		self._resume = Selection("Resume",lambda : self.resume())
		self._retry = Selection("Retry",lambda : self.retry())
		self._options = Selection("Options",lambda : self.options())
		self._main_menu = Selection("Main menu",lambda : self.main_menu())
		self.menus = Menu(
			[self._resume, self._retry, self._options, self._main_menu],
			self.width / 2, self.height / 2
		)

	def resume(self):
		self.window.show_view(self.game_view)

	def retry(self):
		maze = MazeGenerator(config.MAZE_SIZE).maze
		from game import Game
		game_view = Game(maze, self.screen_view)
		self.window.show_view(game_view)

	def options(self):
		from settings import Settings
		set_view = Settings(self, self.game_view)
		self.window.show_view(set_view)

	def	main_menu(self):
		self.window.show_view(self.screen_view)

	def on_update(self, delta_time):
		if self.menus.scale < 2:
			self.menus.scale += delta_time * 3

	def on_key_press(self, symbol, modifiers):
		if symbol == arcade.key.UP:
			self.menus.move_up()
		if symbol == arcade.key.DOWN:
			self.menus.move_down()
		if symbol == arcade.key.ESCAPE:
			self.window.show_view(self.game_view)
		if symbol == arcade.key.ENTER:
			self.menus.action()

	def on_draw(self):
		self.clear()
		self.game_view.on_draw()
		r = arcade.rect.XYWH(self.width / 2, self.height / 2, self.width, self.height)
		arcade.draw_rect_filled(r, (0, 0, 0, 220))
		self.menus.draw_texts()
