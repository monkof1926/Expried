from kivy.uix.screenmanager import Screen
# for makng button work
from kivy.properties import OptionProperty, NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivymd.uix.list import TwoLineAvatarListItem
from kivymd.uix.list import OneLineAvatarListItem
from kivymd.uix.list import OneLineListItem
from kivymd.uix.list import BaseListItem
from kivymd.uix.relativelayout import RelativeLayout
from kivymd.uix.selection import MDSelectionList
from kivymd.uix.selection import SelectionItem
from kivymd.uix.selection import SelectionIconCheck
from kivy.animation import Animation

from kivy.utils import get_color_from_hex

from kivymd.theming import ThemableBehavior
from kivymd.uix.behaviors import TouchBehavior
from kivymd.uix.button import MDIconButton
from kivymd.uix.list import MDList
from kivymd.uix.relativelayout import MDRelativeLayout
from kivy.metrics import dp

from Items import *
from Widgets import *
from Widgets import ScrollViewList
from . import *
class MyItem(TwoLineAvatarListItem):
    def on_long_touch(self, touch):
        self.on_touch_up(touch)
    pass

class ListScreen(MScreen):
    # addItemBtn = ObjectProperty(None)
    def __init__(self,items = None,**kwargs):
        super().__init__(**kwargs)
        # self.addItemBtn.screen = self
        self.items = items


    # kivy func: happens before screen shows
    def on_pre_enter(self, *args):
        # self.addItemBtn.addType(type = "screen_change",screen = self.manager.get_screen("menu"))
        # self.addItemBtn.bindFunctionalities()
        if not self.ids.select_view.fridge:
            self.ids.select_view.initialEnter(self)
        return super().on_enter(*args)

    def on_leave(self, *args):
        self.ids.select_view.refresh_on_exit()
        return super().on_leave(*args)

    def startScreen(self):
        pass




    pass

