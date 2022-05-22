from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivymd.app import MDApp
from Screens.MainMenuScreen import MenuScreen
from Screens.ScanScreen import ScanScreen
from Screens.SettingsScreen import SettingsScreen
from Screens.CalenderScreen import CalenderScreen
from kivy.core.text import LabelBase
from kivy.config import Config
from Items import *
from kivymd.uix.textfield import MDTextField
# from kivymd.uix.transition.transition import MDFadeSlideTransition
# kivymd.uix.transition.transition.MDFadeSlideTransition

LabelBase.register(name='ExpiredFont', fn_regular='Resources/custom.ttf')
Builder.load_file('Screens/listscreen.kv')
Builder.load_file('Screens/mainmenuscreen.kv')
from Screens.ListScreen import ListScreen
Builder.load_file('Widgets/itemlistdisplay.kv')
Builder.load_file('Screens/scanscreen.kv')
Builder.load_file('Widgets/bars.kv')

Builder.load_file('Screens/settingsscreen.kv')
Builder.load_file('Screens/calenderscreen.kv')
# Config.set(' graphics', 'resizable', '0')
# Config.set('graphics', 'height', '600')
# Config.set('graphics', 'width', '300')

# from kivy.core.window import Window

# Window.softinput_mode = "below_target"

import json

# 
class TestApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Green"  # "Purple", "Red"
        self.theme_cls.primary_hue = "200"  # "500"
        self.items = Items("data.json")
        # items.jsonFo rmatToItemFormat()
        self.items.openFridge()
        sm = ScreenManager()
        self.sm = sm
        sm.fridge = self.items # so it can be accessed by other screens
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(ListScreen(name='list'))
        sm.add_widget(ScanScreen(name='scan'))
        sm.add_widget(SettingsScreen(name='settings'))
        sm.add_widget(CalenderScreen(name='calender'))
        return sm

TestApp().run()



# cake = Item("Cake",Date(2530,5,9),"4")
# pizza = Item("Pizza",Date(2050,2,6),"2")

# fridge = Items(jsonfile = "data.json")
# fridge.addItem(cake)
# fridge.addItem(pizza)
# fridge.sortAscendingDate()
# fridge.convertToJSON()
# jsondic = fridge.createJSON()


# dic = fridge.loadJSON()
# fridge.jsonFormatToItemFormat(dic)
# items = Items("data copy.json")
# items.jsonFormatToItemFormat()
# print(items.fridge)
# items.removeItem("5")
# print(items.fridge)
# # items.convertToJSON()
# # items.createJSON()
