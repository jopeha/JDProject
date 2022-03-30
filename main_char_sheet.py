from kivy.config import Config
Config.set('graphics', 'resizable', '0') #0 being off 1 being on as in true/false
Config.set('graphics', 'width', '426')
Config.set('graphics', 'height', '900')


import Generators
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ListProperty, NumericProperty, StringProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.animation import Animation
from random import gauss
import threading
from kivy.clock import Clock
from kivy.utils import get_color_from_hex

SS = """
#:import utils kivy.utils
#:set hx utils.get_color_from_hex
#:set font_size 20
#:set row_padding 10
#:set bg1col hx("#022436")
#:set bg2col hx("#012F46")
#:set fontcol hx("#EDF7D2")
#:set h1col hx("#842C2A")
#:set h2col hx("#c23D2A")
#:set h3col hx("#EA8A44")


    
<Parname@Label>
    text:self.parent.__class__.__name__
    
    
<CLabel@Label>
    size_hint_y:None
    size_hint_x:None
    font_size:font_size
    height:font_size+row_padding*2
    font_name:"RobotoMono-Regular"
    width:len(self.text)*font_size*0.6+row_padding*2
    
<OneLineInput@TextInput>
    valign:"center"
    multiline:False
    size_hint_y:None
    font_size:font_size
    height:font_size+row_padding*2
    font_name:"RobotoMono-Regular"

<NumInput@OneLineInput>
    size_hint_x:None
    width: font_size*2
    halign:"center"

<Row@BoxLayout>
    size_hint_y:None
    height:font_size+row_padding*2
<CButton@Button>
    size_hint_y:None
    size_hint_x:None
    font_size:font_size
    height:font_size+row_padding*2
    font_name:"RobotoMono-Regular"
    width:len(self.text)*font_size*0.6+row_padding*2
     
<DDButton@Button>
    size_hint_y:None
    size_hint_x:None
    font_size:font_size
    height:font_size+row_padding*2
    font_name:"RobotoMono-Regular"
    ddoptions:["1","2","3"]
    width:max(map(lambda a: len(a),self.ddoptions))*font_size+row_padding*2
     

<StartScreen>
    name:"Start"
    Parname:
<LoadScreen>
    name:"Load"
    Parname:
<CharScreen>
    name:"Char"
    id:char
    BoxLayout:
        padding:20
        spacing:10
        orientation:"vertical"
        Row:
            CLabel:
                text:"Name"
            OneLineInput:
                size_hint_x:None
                width:max(font_size*6,row_padding*2+len(self.text)*font_size*.6)
            Widget
        Row:
            CLabel:
                text:"Age"
            NumInput:        
            CLabel:
                text:"Fame"
            NumInput:

            OneLineInput:
        Row:
            DDButton:
                id:type
                text:"Human"
                ddoptions:["Human","Cyborg","Mutant"]
                width:max(map(lambda a: len(a),self.ddoptions))*font_size+row_padding*2
            CLabel:
                text:"Bulk:"
            CLabel:
                text:str(bt.value)
            Slider:
                id:bt
                min:-2 if type.text!="Human" else -1
                max:2 if type.text!="Human" else 1
                value:3
                step:1
        Button:

"""
class DDButton(Button):
    def __init__(self,**kwargs):
        super(DDButton, self).__init__(**kwargs)
        self.on_release=self.showDropdown



    def showDropdown(self):
        self.dd=DropDown()
        for i in self.ddoptions:
            btn = Button(text=i,size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: self.dd.select(btn.text))
            self.dd.add_widget(btn)
        self.dd.bind(on_select=lambda instance, x: setattr(self, 'text', x))
        self.dd.open(self)


class TypeDD(DropDown):
    pass

class StartScreen(Screen):
    pass
class LoadScreen(Screen):
    pass
class CharScreen(Screen):
    dropdowns = {
        "TYPE": TypeDD()
    }


class BlocksplorerApp(App):

    def build(self):
        self.sm = ScreenManager()
        Builder.load_string(SS)

        self.ss, self.ls, self.cs = StartScreen(), LoadScreen(), CharScreen()

        self.sm.add_widget(self.ss)
        self.sm.add_widget(self.ls)
        self.sm.add_widget(self.cs)

        self.sm.current="Char"

        return self.sm



if __name__ == "__main__":
    app = BlocksplorerApp()
    app.run()
