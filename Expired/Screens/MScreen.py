from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivymd.uix.screen import MDScreen


class MScreen(MDScreen):
    app = App.get_running_app()
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs) 
    def closeApp(self):
        App.get_running_app().stop()