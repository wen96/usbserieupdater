import kivy
kivy.require('1.8.0')

from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from kivy.lang import Builder

from kivy.config import Config
Config.set('kivy', 'window_icon', 'icon.png')
Config.set('graphics', 'height', 600)
Config.set('graphics', 'width', 800)


class MainScreen(Screen):
    info = StringProperty()

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

    def do_action(self):
        self.info = 'New info text'

    Builder.load_file('views/home.kv')


class MainApp(App):
    title = 'Ouuuuu yeah!'

    def build(self):
        return MainScreen(info='Hello world')

if __name__ == '__main__':
    MainApp().run()
