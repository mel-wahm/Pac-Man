import arcade
regular_fruits = arcade.load_texture("fruits/super_fruit_green.png")
class	Fruits(arcade.View):
	def __init__(self, fruit: arcade.Texture) -> None:
		super().__init__()
		self.background_color = (20, 20, 40)
		self.fruit = arcade.Sprite(fruit)
		self.fruit.center_x = self.width / 2
		self.fruit.center_y = self.height / 2
		# self.fruit.scale = 100
		self.fruits = arcade.SpriteList()
		self.fruits.append(self.fruit)

	def on_update(self, delta_time):
		self.fruit.scale = min(3, self.fruit.scale_x + delta_time * (1 / self.fruit.scale_x))
	def on_key_press(self, symbol: int, modifiers: int) -> None:
		if symbol == arcade.key.Q:
			exit()

	def on_draw(self) -> None:
		self.clear()
		self.fruits.draw()

W = arcade.Window(1980, 1080, "", True)
W.show_view(Fruits(regular_fruits))
arcade.run()
