from kivymd.uix.relativelayout import RelativeLayout
from kivymd.uix.list import BaseListItem
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.dialog import MDDialog
from kivy.uix.popup import Popup
from kivy.uix.modalview import ModalView
from kivymd.uix.button import MDFlatButton
from kivymd.uix.list import OneLineListItem
from kivymd.uix.menu import MDDropdownMenu
from kivy.core.window import Window
"""Class that uses the abstract MD BaseListItem. 
Used when adding a widget to the item list
"""

class ListItemBase(BaseListItem):
    pass

class FoodItemSelection(ListItemBase):
    def __init__(self,item = None, _owner = None):
        self.item = item
        self._owner = _owner
        super().__init__()
    def createOption(self):
        self.ids.list_item.exp_date_lbl = self._owner.expiryDate.toString_DMY()
        self.ids.list_item.product_name_lbl = self._owner.productName

    def __repr__(self):

        return str(self._owner.productName)
""" Hold lists of widgets - includes the list in Items and ItemViewList """
class ItemWidgetList():
    def __init__(self,fridge = None):
        self.fridge = fridge
        self.sorted_fridge_list = []
        self.sort_date()
    
    def __iter__(self):
        for item in self.sorted_fridge_list:
            yield item

    def sort_date(self,ascending = True):
        self.sorted_fridge_list = sorted(self.sorted_fridge_list,reverse=not ascending, key=lambda x: (x._owner.expiryDate,x._owner.productName.casefold()))

    def sort_name(self,ascending = True):
        self.sorted_fridge_list = sorted(self.sorted_fridge_list,reverse=not ascending, key=lambda x: (x._owner.productName.casefold(),x._owner.expiryDate))
    
    def append(self,item):
        self.sorted_fridge_list.append(item)
    
    def remove(self,item):
        self.sorted_fridge_list.remove(item)
        
    def clear(self):
        self.sorted_fridge_list.clear()

    def copy(self):
        return self.sorted_fridge_list.copy()

    def refill_list(self,list):
        self.sorted_fridge_list.clear()
        for widget in list:
            self.sorted_fridge_list.append(widget)
    pass



class MSnackbar(Snackbar):
    pass

class ConfirmDelete(MDDialog):
    
    def __init__(self, _parent = None, deleted_items = None, **kwargs):
        self.cancel_button = MDFlatButton(
                text="CANCEL",
                theme_text_color="Custom",
                # text_color=self.theme_cls.primary_color,
                on_release= self.dismiss,
            )
        self.ok_button = MDFlatButton(
                text="CONFIRM",
                theme_text_color="Custom",
                # text_color=self.theme_cls.primary_color,
                on_release= self.confirmButton,
            )
        buttons=[
            self.cancel_button, self.ok_button
        ]
        # self.deleted_items = deleted_items
        self.findItems(deleted_items)
        super().__init__(buttons = buttons, **kwargs)
        self._parent = _parent
        
    def confirmButton(self,intsance):
        self._parent.delete_items()
        self.dismiss()

    def findItems(self,items):
        self.text = ""; noofitems = 0
        for item in items:
            noofitems += 1
            self.text += f"{item.instance_item._owner.toString()}"
            if noofitems >= 3:
                self.text += "\n..."
                break
            elif len(items) > noofitems:
                self.text += "\n"

class ListItem(OneLineListItem):
    divider = None
    pass

""" The part that handles the whole list area
"""
class ItemListView(RelativeLayout):

    list_of_items = []
    list_of_items_sorted = []
    current_widgets = []
    current_widgets = []
    fridge = None

    def initialEnter(self,screen):
        self.screen = screen
        self.fridge = self.screen.manager.fridge
        self.widgets = self.fridge.widget_list
        self.selection_list = self.ids.selection_list
        self.current_widgets = ItemWidgetList()
        self.add_all_items()
        self.displayWidgets()

    """ Not sure what this was for. Does literally nothing. """
    def refresh_on_exit(self):
        self.widgets = self.fridge.widget_list
        self.displayWidgets()

    """ Adds the widgets to the list view widget """
    def displayWidgets(self):
        self.ids.selection_list.clear_widgets()
        for item in self.current_widgets:
            self.ids.selection_list.add_widget(item)


    """Just adds all items to the list view"""
    def add_all_items(self):
        self.current_widgets.clear()
        for item in self.fridge:
            option = item.food_item_selection
            option.createOption()
            self.current_widgets.append(option)

    """Give it the list of items you want the list to show"""
    def refreshWidgets(self):
        self.ids.selection_list.clear_widgets()
        for widget in self.current_widgets:
            self.ids.selection_list.add_widget(widget)

    """Sorts the list view by date"""
    def sortDate(self,ascending = True):
        self.current_widgets.sort_date(ascending=ascending)
        self.refreshWidgets()

    """Sorts the list view by name"""
    def sortName(self,ascending = True):
        self.current_widgets.sort_name(ascending=ascending)
        self.refreshWidgets()

    """Deletes the items selected by user
    ATTENTION: should maybe have a snackbar for when people press the delete and nothing is selected"""
    def deleteSelectedItems(self):
        items = self.ids.selection_list.get_selected_list_items()
        if not items:
            MSnackbar().open()
        else:
            delete_dialog = ConfirmDelete(_parent = self,deleted_items = items)
            delete_dialog.open()
    
    def delete_items(self):
        items = self.ids.selection_list.get_selected_list_items()
        for item in items:
            print(type(item.instance_item._owner))
            self.screen.manager.fridge.removeItem(item.instance_item._owner)
            self.current_widgets.remove(item.instance_item._owner.food_item_selection)
            self.ids.selection_list.remove_widget(item)

    def resetList(self):
        pass

    """ Adds back all the items to the current widgets list"""
    def refreshList(self):
        self.current_widgets.refill_list(self.widgets)
        self.ids.toolbar.title = "Items"
        # self.list_of_widgets.clear()
        # for widget in self.widgets:
        #     self.list_of_widgets.append(widget)baselistitem
        
        self.refreshWidgets()

    """ Checks for which items contain searched string and adds it to the list widget """
    def stringSearch(self,string):
        # self.list_of_widgets.refill_list(self.widgets)
        self.selection_list.clear_widgets()
        for widget in self.current_widgets.copy():
            r = widget._owner.productName.find(string)
            if r==-1:
                self.current_widgets.remove(widget)
        self.refreshWidgets()
    
    def searchItems(self):
        search_input = self.ids.search_popup.ids.search_field.text
        self.stringSearch(search_input)
        
    def openSortBy(self):
        SortByPopup(_parent = self).open()
        self.refreshWidgets()
    
    def openSearch(self):
        # self.list_of_widgets.refill_list(self.widgets)
        self.refreshList()
        # self.displayWidgets()
        text_popup = SearchPopup(_parent = self).open()


class SortByPopup(Popup):
    
    def __init__(self, _parent = None, **kwargs):
        super().__init__(**kwargs)
        self._parent =  _parent
    
    pass
      
class SearchPopup(ModalView):
    def __init__(self, _parent = None, **kwargs):
        super().__init__(**kwargs)
        self._parent =  _parent

    # def on_enter(self):
    #     self.clickedSearch()

    def clickedSearch(self):
        search_text = self.ids.search_field.text
        self._parent.stringSearch(search_text)
        self._parent.ids.toolbar.title = search_text
        self.dismiss()
        pass