import arcade
from game import Game
from mazegenerator import MazeGenerator
from settings import Settings
from menu import Selection, Menu

class Screen(arcade.View):
	def __init__(self):
		super().__init__()
		self.wallpaper = arcade.load_texture("wallpaper/wallpaper.png")
		arcade.load_font("fonts/arcade_font.ttf")
		arcade.load_font("fonts/Renogare-Regular.otf")
		self.cx, self.cy = self.width / 2, self.height / 2
		self.start = Selection("Start", lambda: self.start_game())
		self.settings = Selection("Settings", lambda: self.enter_settings())
		self.exit = Selection("Exit", lambda: self.exit_game())
		self.menus = Menu([self.start, self.settings, self.exit],
					self.width / 2, self.height / 2)
		maze = MazeGenerator((13, 7)).maze
		self.game_view = Game(maze, self)

	def start_game(self):
		self.window.show_view(self.game_view)
	def enter_settings(self):
		settings_view = Settings(self, self.game_view)
		self.window.show_view(settings_view)
	def exit_game(self):
		exit()
		
	def on_key_press(self, symbol, modifiers):
		if symbol == arcade.key.Q:
			exit()
		if symbol == arcade.key.DOWN:
			self.menus.move_down()
		if symbol == arcade.key.UP:
			self.menus.move_up()
		if symbol == arcade.key.ENTER:
			self.menus.action()

	def on_draw(self):
		self.clear()
		r = arcade.rect.XYWH(self.width / 2, self.height / 2, self.width, self.height)
		arcade.draw_texture_rect(self.wallpaper, r)
		self.menus.draw_texts()
