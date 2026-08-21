import arcade


class Selection:
    """Class to create an instance of a menu"""

    def __init__(self, name, action):
        self.name = name
        self.action = action


class Menu:
    """Class to store all instance of menus"""

    def __init__(self, menus, x, y, gap=65, font_size=35):
        self.menus = menus
        self.x, self.y = x, y
        self.gap = gap
        self.font_size = font_size
        self.select = 0
        self.texts = []
        self.scale = 1
        total_height = (len(menus) - 1) * gap
        for i in range(len(menus)):
            self.texts.append(
                arcade.Text(
                    self.menus[i].name,
                    self.x,
                    self.y + total_height / 2 - (i * self.gap),
                    arcade.color.WHITE,
                    self.font_size,
                    anchor_x="center",
                    font_name="Renogare",
                )
            )

    def mouse_motion(self, x, y, menu):
        for i in range(len(menu.menus)):
            if (
                menu.texts[i].left < x < menu.texts[i].right
                and menu.texts[i].bottom < y < menu.texts[i].top
            ):
                menu.select = i

    def mouse_press(self, x, y, menu):
        for i in range(len(menu.menus)):
            if (
                menu.texts[i].left < x < menu.texts[i].right
                and menu.texts[i].bottom < y < menu.texts[i].top
            ):
                menu.menus[i].action()

    def move_up(self):
        self.select = (self.select - 1) % len(self.menus)
        self.scale = 1

    def move_down(self):
        self.select = (self.select + 1) % len(self.menus)
        self.scale = 1

    def action(self):
        self.menus[self.select].action()

    def draw_texts(self):
        for i in range(len(self.menus)):
            if i == self.select:
                self.texts[i].color = arcade.color.YELLOW
                self.texts[i].font_size = self.font_size * min(1.5, self.scale)
            else:
                self.texts[i].color = arcade.color.WHITE
                self.texts[i].font_size = self.font_size
            self.texts[i].draw()
