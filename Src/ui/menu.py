import arcade


class Selection:
    """Represents a single selectable menu item with a display label and action callback."""

    def __init__(self, name: str, action):
        self.name = name
        self.action = action


class Menu:
    """Manages a vertical list of menu items with keyboard and mouse navigation."""

    def __init__(self, items: list[Selection], x: float, y: float, gap: float = 65, font_size: int = 35):
        self.menus = items
        self.x = x
        self.y = y
        self.gap = gap
        self.font_size = font_size
        self.selected_index = 0
        self.labels = []
        self.scale = 1.0

        total_height = (len(items) - 1) * gap
        for i, item in enumerate(items):
            item_y = self.y + total_height / 2 - (i * self.gap)
            self.labels.append(
                arcade.Text(
                    item.name,
                    self.x,
                    item_y,
                    arcade.color.WHITE,
                    self.font_size,
                    anchor_x="center",
                    font_name="Renogare",
                )
            )

    def mouse_motion(self, x: float, y: float, menu=None):
        target = menu or self
        for i, label in enumerate(target.labels):
            if label.left < x < label.right and label.bottom < y < label.top:
                target.selected_index = i

    def mouse_press(self, x: float, y: float, menu=None):
        target = menu or self
        for i, label in enumerate(target.labels):
            if label.left < x < label.right and label.bottom < y < label.top:
                target.menus[i].action()

    def move_up(self):
        self.selected_index = (self.selected_index - 1) % len(self.menus)
        self.scale = 1.0

    def move_down(self):
        self.selected_index = (self.selected_index + 1) % len(self.menus)
        self.scale = 1.0

    def action(self):
        self.menus[self.selected_index].action()

    def draw_texts(self):
        for i, label in enumerate(self.labels):
            if i == self.selected_index:
                label.color = arcade.color.YELLOW
                label.font_size = self.font_size * min(1.5, self.scale)
            else:
                label.color = arcade.color.WHITE
                label.font_size = self.font_size
            label.draw()

    def draw(self):
        self.draw_texts()
