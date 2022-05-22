import time
import datetime as dt

from Widgets.ItemListDisplay import ItemWidgetList
# import Item
from . import Date
from . import Item
import json
# import Data
import os


class Items():


    def __init__(self,jsonfile = "NaN"):
        self.fridge = {}
        self.sortedFridgeListDate = []
        self.sortedFridgeListName = []
        # self.widget_list = []
        self.widget_list = ItemWidgetList()
        self.jsonfile = jsonfile
        self.jsonDict = None # Dictionary of items but in the format for a JSON file
        self.loadJSON()

    def __iter__(self):
        for key,item in self.fridge.items():
            yield item

    """ Saves an item to the current lists and to the JSON file """
    def addItemToFridge(self,item):
        item.createUniqueID()
        while item.ID in self.fridge.keys():
            item.createUniqueID()
        self.addItemToLists(item)
        self.convertToJSON()
        self.createJSON()

    """ Adds items to the current lists and dictionaries"""
    def addItemToLists(self,item:Item):
        self.fridge[item.ID] = item
        self.sortedFridgeListDate.append(item)
        self.sortedFridgeListName.append(item)
        self.widget_list.append(item.food_item_selection)
        self.sortAscendingDate()
        self.sortProductName()

    """ Deletes item from lists and JSON file """
    def removeItem(self, itemID):
        # print(type(itemID))
        self.fridge.pop(itemID.ID)
        self.jsonDict.pop(itemID.ID)
        self.widget_list.remove(itemID.food_item_selection)
        self.convertToJSON()
        self.createJSON()

    """ Adds an item to the json dictionary with the format accepted by json files """
    def convertToJSON(self):
        for item in self.fridge.values():
            self.jsonDict[item.ID] = item.convertToJSONInput()

    """ Rewrites the current json file with the current json dictionary"""
    def createJSON(self):
        with open(self.jsonfile, 'w') as f:
            json.dump(self.jsonDict,f)

    """ Loads the JSON file and saves it in the json dict format """
    def loadJSON(self):
        f = open(self.jsonfile)
        q = json.load(f)
        self.jsonDict = q
        return q

    """ The method called outside to load the JSON file into the current running time """
    def openFridge(self):

        self.jsonFormatToItemFormat()

    """ Takes the json dict and formats it into Item format """
    def jsonFormatToItemFormat(self,jsonitem = None):
        self.loadJSON()
        for key,value in self.jsonDict.items():
            item  = Item(value[0],Date(value[1][0],value[1][1],value[1][2]),key)
            self.addItemToLists(item)

    """ Sorting the sorted lists for after adding items """
    def sortAscendingDate(self):    
        self.sortedFridgeListDate = sorted(self.sortedFridgeListDate, key=lambda x: (x.expiryDate,x.productName.casefold()))
        # self.widget_list = sorted(self.widget_list, key=lambda x: (x.owner.expiryDate,x.owner.productName.casefold()))
        self.widget_list.sort_date()

    def sortProductName(self):
        self.sortedFridgeListName = sorted(self.sortedFridgeListName, key=lambda x: (x.productName.casefold(),x.expiryDate))

    def toString(self):
        strs = ""
        for item in self.fridge.values():
            strs = f"{strs + item.toString()}\n"
        return strs

    """ Probably unnecessary - depends on where we want to store out data"""
    def createJSONrel(self):
        cur_path = os.path.dirname(__file__)
        new_path = os.path.relpath('..\\Data\\data.json', cur_path)

        with open(new_path, 'w') as f:
            json.dump(self.jsonDict,f)

    def loadJSONrel(self):
        cur_path = os.path.dirname(__file__)
        new_path = os.path.relpath('..\\Data\\' + self.jsonfile, cur_path)

        with open(new_path, 'r') as f:
            q = json.loads(f.read())
            return q

