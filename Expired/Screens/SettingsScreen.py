from kivy.uix.screenmanager import Screen
from . import MScreen
from kivy.utils import platform
from kivy.network.urlrequest import UrlRequest

class SettingsScreen(MScreen):
    pass
"""
if platform == ('win'):
    from textractcaller import call_textract
    import os
    from trp import Document

class SettingsScreen(MScreen):
    
    def apiTEST(self):

        if platform == "win":
            SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
            input_file = os.path.join(SCRIPT_DIR, "testdate2.png")
            with open(input_file, "rb") as sample_file:
                b = bytearray(sample_file.read())
                j = call_textract(input_document=b)
                assert j
                doc = Document(j)
                assert doc
                print(doc)
    

    def apiTEST2(self):
        request = UrlRequest("https://catfact.ninja/fact", on_success=self.get_data)

    def get_data(self,request,response):
        self.ids.labelText.text = response['fact']
"""