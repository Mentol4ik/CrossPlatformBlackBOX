from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

from game import my_game
from game.app import GameInterface


class BlackBoxGame(BoxLayout):
    def __init__(self, **kwargs):
        self.game: "GameInterface" = my_game

        super().__init__(orientation="vertical", **kwargs)

        self.add_widget(Label(text="Welcome to BLACKBOX!", font_size=24))
        self.output_label = Label(
            text="Place your atoms and fire rays!", size_hint_y=None, height=50
        )
        self.add_widget(self.output_label)

        self.input = TextInput(
            hint_text="Enter ray number (1-32)",
            multiline=False,
            size_hint_y=None,
            height=40,
        )
        self.add_widget(self.input)

        self.fire_button = Button(
            text="Fire Ray", on_press=self._on_fire_ray, size_hint_y=None, height=50
        )
        self.add_widget(self.fire_button)

    def _on_fire_ray(self, instance):
        """Обработчик нажатия кнопки Fire Ray."""
        ray_input = self.input.text.strip()
        if not ray_input.isdigit():
            self.output_label.text = "Invalid input! Please enter a valid number."
            return

        ray = int(ray_input)
        if ray == 0:
            self.output_label.text = "Guess phase starting soon!"
            self.input.text = ""
            return

        if not (1 <= ray <= 32):
            self.output_label.text = "Invalid input! Please enter a number between 1 and 32."
            self.input.text = ""
            return

        # Вызов метода игры
        self.output_label.text = self.game.play(ray)
        self.input.text = ""


class BlackBoxApp(App):
    def build(self):
        return BlackBoxGame()


if __name__ == "__main__":
    BlackBoxApp().run()
