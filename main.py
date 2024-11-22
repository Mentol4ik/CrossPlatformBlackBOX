from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import random


# Функция для создания случайной координаты
def random_coordinate():
    return random.randint(1, 8)


# Функция для получения направления луча в зависимости от выбранной грани
def get_ray_direction(ray):
    if 1 <= ray <= 8:
        return (0, 1), ray, 0  # Левая сторона (X=0)
    elif 9 <= ray <= 16:
        return (1, 0), 9, ray - 8  # Нижняя сторона (Y=9)
    elif 17 <= ray <= 24:
        return (0, -1), 9 - (ray - 16), 9  # Правая сторона (X=9)
    elif 25 <= ray <= 32:
        return (-1, 0), 0, 33 - ray  # Верхняя сторона (Y=0)


class BlackBoxGame(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.grid_size = 9
        self.atoms_count = 5
        self.grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.score = 0
        self.found_atoms = 0

        # Генерация атомов
        for _ in range(self.atoms_count):
            while True:
                x, y = random_coordinate(), random_coordinate()
                if self.grid[x][y] == 0:
                    self.grid[x][y] = 1
                    break

        self.add_widget(Label(text="Welcome to BLACKBOX!", font_size=24))
        self.output_label = Label(text="Place your atoms and fire rays!", size_hint_y=None, height=50)
        self.add_widget(self.output_label)

        self.input = TextInput(hint_text="Enter ray number (1-32)", multiline=False, size_hint_y=None, height=40)
        self.add_widget(self.input)

        self.fire_button = Button(text="Fire Ray", on_press=self.fire_ray, size_hint_y=None, height=50)
        self.add_widget(self.fire_button)

    def fire_ray(self, instance):
        try:
            ray = int(self.input.text)
            if ray == 0:
                self.output_label.text = "Guess phase starting soon!"
                return

            direction, x, y = get_ray_direction(ray)
            dx, dy = direction

            while 0 <= x < self.grid_size and 0 <= y < self.grid_size:
                if self.grid[x][y] == 1:
                    self.output_label.text = "ABSORBED!"
                    self.score += 1
                    return
                if (
                    0 <= x + dx < self.grid_size
                    and 0 <= y + dy < self.grid_size
                    and (self.grid[x + dx][y] == 1 or self.grid[x][y + dy] == 1)
                ):
                    dx, dy = -dx, -dy
                    self.output_label.text = "REFLECTED!"
                else:
                    x += dx
                    y += dy

            if not (0 <= x < self.grid_size and 0 <= y < self.grid_size):
                self.output_label.text = "ESCAPED!"
        except ValueError:
            self.output_label.text = "Invalid input! Please enter a number."

        self.input.text = ""


class BlackBoxApp(App):
    def build(self):
        return BlackBoxGame()


if __name__ == "__main__":
    BlackBoxApp().run()
