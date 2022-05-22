from audioop import tostereo
from kivy.uix.screenmanager import Screen
from . import MScreen
from kivy.app import App

# for makng button work
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
# from ..Widgets.Button import Button
# from ..Items.Items import Items
from kivy.uix.button import Button
from functools import partial


def changeScreen(fromScreen,toScreen):
    fromScreen.manager.current = toScreen.name
    toScreen_ = fromScreen.manager.current_screen
    toScreen_.startScreen()

class TestScreen():
    def screenChange(self,toScreen):
        changeScreen(self,toScreen)

    pass


class MenuScreen(MScreen,TestScreen):
    gotolist = ObjectProperty(None)
    def __init__(self,**args):
        super().__init__(**args)
        # self.gotolist.bind(on_press=partial(self.screenChange()))


    

    def changeToList(self):
        self.manager.current = 'list'
        listscreen = self.manager.current_screen
        listscreen.startScreen()



    pass





class Btn(Button):
    def __init__(self,screen):
        self.screen = screen

    def changeScreen(self,toScreen):

        pass



