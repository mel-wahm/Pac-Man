import arcade
regular_fruits = arcade.load_texture("fruits/super_fruit.png")
class	Fruits(arcade.View):
	def __init__(self, fruit: arcade.Texture) -> None:
		super().__init__()
		self.background_color = (20, 20, 40)
		self.fruit = fruit

	def on_key_press(self, symbol: int, modifiers: int) -> None:
		if symbol == arcade.key.Q:
			exit()

	def on_draw(self) -> None:
		self.clear()
		r = arcade.rect.XYWH(self.width / 2,
							 self.height / 2,
							 142, 142)
		arcade.draw_texture_rect(self.fruit, r)

W = arcade.Window(1980, 1080, "", True)
W.show_view(Fruits(regular_fruits))
arcade.run()