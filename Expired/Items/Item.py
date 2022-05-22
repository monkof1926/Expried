from Widgets.ItemListDisplay import FoodItemSelection
from . import Date
from random import randint
from Widgets import *

class Item():
    
    def __init__(self,productName = "NaN",expiryDate=Date(2000,1,1), ID = "Invalid"):
        self.productName = productName
        self.expiryDate  = expiryDate
        self.ID          = ID
        self.food_item_selection = FoodItemSelection(_owner = self)
        # self.food_item_selection = None

    """ Generates an ID for an item with 4 random digits"""
    def createUniqueID(self):
        ID = str(randint(1000,4999))
        self.ID = self.productName + ID

    """ Arranges the information so it can be stored in the JSON file """
    def convertToJSONInput(self):
        return [self.productName,[self.expiryDate.year,self.expiryDate.month,self.expiryDate.day]]

    """ In order for displaying the item """
    def toString(self):
        return f"{self.productName} - exp: {self.expiryDate}"











    





