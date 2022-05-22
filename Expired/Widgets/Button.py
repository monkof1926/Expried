from kivy.uix.button import Button
from kivy.app import App
from functools import partial
import sys
# sys.path.append("./Items")
# sys.path.append("./Widgets")
# sys.path.append("./Items")
# sys.path.append("./Items/Date")

from Items import *
from Widgets import *


class MBtn(Button):
    # screen = None
    # items = None
    app = App.get_running_app() 
    def __init__(self,screen = None,**kwargs):
        super().__init__(**kwargs)
        print("jfjfj")
        self.screen = screen
        self.listOfTypes = []
    def printer(self):
        # item = Item("")
        pizza = Item("cookies",Date(2050,2,6),"5")
        self.screen.manager.app.items.addItem(pizza)
        print("woohooo")
    def addType(self,type = None,**typeargs):
        self.listOfTypes.append(BtnType(type,**typeargs))
        pass

    def addItem(self,item,fridge = None):
        self.app.items.addItem(item)
        pass

    def changeScreen(self,instance,screen = None):
        print("it works woohooo")
        self.screen.manager.current = screen
        pass

    def customBind(self,func,**funcargs):
        self.bind(on_press=partial(func,**funcargs))
        pass

    def bindFunctionalities(self):
        for btntype in self.listOfTypes:
            if btntype.type == "screen_change":
                self.customBind(self.changeScreen,screen = btntype.screen.name)
            pass
        pass


class BtnType:
    def __init__(self,type = "NoneType",**typeargs):
        self.type = type
        for key,value in typeargs.items():
            setattr(self,key,value)
        pass
    pass