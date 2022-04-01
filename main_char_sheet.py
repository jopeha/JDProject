from kivy.config import Config

Config.set('graphics', 'resizable', '0')  # 0 being off 1 being on as in true/false
Config.set('graphics', 'width', '426')
Config.set('graphics', 'height', '900')

from kivy.uix.image import Image
from os.path import exists
import json
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
from kivy.clock import Clock
from functools import partial
import kivy.utils as utils

hx = utils.get_color_from_hex
font_size = 20
row_padding = 10
bg1col = hx("#022436")
bg2col = hx("#012F46")
bg3col = hx("#184257")
bg4col = hx("#3C6169")
fontcol = hx("#EDF7D2")
font2col = hx("#77938C")
h1col = hx("#842C2A")
h2col = hx("#c23D2A")
h3col = hx("#EA8A44")

SS = """
#:import utils kivy.utils
#:set hx utils.get_color_from_hex
#:set font_size 20
#:set row_padding 10
#:set bg1col hx("#022436")
#:set bg2col hx("#012F46")
#:set bg3col hx("#184257")
#:set bg4col hx("#3C6169")
#:set fontcol hx("#EDF7D2")
#:set font2col hx("#77938C")
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
    width:max(2,len(self.text))*font_size*0.6+row_padding*2
    color:fontcol
    text:"0"

<OneLineInput@TextInput>
    valign:"center"
    multiline:False
    size_hint_y:None
    font_size:font_size
    height:font_size+row_padding*2
    font_name:"RobotoMono-Regular"
    foreground_color:bg1col
    disabled_foreground_color:fontcol
    background_normal:"font2col.png"
    background_disabled_normal:"bg2col.png"
    background_active:"fontcol.png"

<NumInput@OneLineInput>
    size_hint_x:None
    width: font_size*2
    halign:"center"
    text:"0"

<Row>
    size_hint_y:None
    r:1
    height:font_size*self.r+row_padding*2

<Slot>
    r:4
    titletext:"Slot name"
    boxwidth:.4
    quality:""
    on_quality:root.parent.parent.parent.parent.do_phage()
    size_hint_x:None
    width:self.parent.width*self.boxwidth if self.parent else 10
    description:""
    canvas:
        Color:
            rgba:bg3col
        Rectangle:
            pos:self.pos
            size:self.width*self.boxwidth,self.height
    BoxLayout:
        padding:5
        orientation:"vertical"
        spacing:5
        Row:
            spacing:5
            CLabel:
                text:root.titletext
            CLabel:
                font_size:15
                text:"Quality"
            NumInput:
                id:quality
                on_text:setattr(root,"quality",self.text)
                text:root.quality

            Widget:

        OneLineInput:
            size_hint_x:None
            width:max(font_size*6,row_padding*2+len(self.text)*font_size*.6)
            on_text:setattr(root,"description",self.text)
            text:root.description



<AugSlot>
    r:4
    titletext:"Slot name"
    boxwidth:1
    quality:""
    size_hint_x:None
    width:self.parent.width*self.boxwidth if self.parent else 10
    description:""
    on_quality:root.parent.parent.parent.parent.do_phage()
    canvas:
        Color:
            rgba:bg3col
        Rectangle:
            pos:self.pos
            size:self.width*self.boxwidth,self.height
    BoxLayout:
        padding:5
        orientation:"vertical"
        spacing:5
        Row:
            spacing:5
            CLabel:
                text:root.titletext
            CLabel:
                font_size:15
                text:"Quality"
            NumInput:
                id:quality
                on_text:setattr(root,"quality",self.text)
                text:root.quality
            Widget:

            CButton:
                text:"x"
                on_release:root.parent.parent.parent.parent.augments.remove(root)
                
        OneLineInput:
            id:description
            size_hint_x:None
            width:max(font_size*6,row_padding*2+len(self.text)*font_size*.6)
            on_text:setattr(root,"description",self.text)
            text:root.description

<BigSlot>
    boxwidth:1
<MedSlot>
    boxwidth:.7
<SmallSlot>
    boxwidth:.73

<CButton>
    size_hint_y:None
    size_hint_x:None
    font_size:font_size
    height:font_size+row_padding*2
    font_name:"RobotoMono-Regular"
    width:len(self.text)*font_size*0.6+row_padding*2
    color:fontcol
    background_color:bg2col
    background_normal:""
    background_disabled_normal:""
    background_disabled_normal:""
<AddAugButton@CButton>
<SepLine>
    size_hint_y:None
    height:5
    canvas:
        Color:
            rgba:bg3col
        Rectangle:
            size:self.size
            pos:self.pos

<DDButton@Button>

    ddoptions:["1","2","3"]

    on_release:self.showDropdown()

<CharScreen>
    name:"Char"
    id:char
    edit_bio:edit_tickbox.state=="down"
    eqbox:eqbox
    phage:"0"

    physical:0
    fitness:"0"
    focus:"0"
    cname:""
    age:"0"
    type:"Human "
    fame:"1"
    famename:""





    canvas:
        Color:
            rgba:bg1col
        Rectangle:
            pos:self.pos
            size:self.size

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
                disabled:root.edit_bio
                id:name
                on_text:setattr(root,"cname",self.text)
                text:root.cname
            Widget
        Row:
            CLabel:
                text:" Age"
            NumInput:
                disabled:root.edit_bio
                id:age
                on_text:setattr(root,"age",self.text)
                text:root.age
            CLabel:
                text:"Fame"
            NumInput:
                disabled:root.edit_bio
                id:fame
                on_text:setattr(root,"fame",self.text)
                text:root.fame
            Widget:
                size_hint_x:None
                width:5
            OneLineInput:
                disabled:root.edit_bio
                id:famename
                on_text:setattr(root,"famename",self.text)
                text:root.famename
        Row:
            DDButton:
                id:type
                text:"Human "
                ddoptions:["Human ","Cyborg","Mutant"]
                disabled:root.edit_bio
                on_text:setattr(root,"type",self.text)
                text:root.type
            CLabel:
                text:"Body"



            Slider:
                id:physical
                min:1 if type.text!="Human " else 2
                max:5 if type.text!="Human " else 4
                value:root.physical
                step:1
                disabled:root.edit_bio
                cursor_image:"fontcol.png"
                cursor_disabled_image:"font2col.png"
                cursor_width:15
                background_disabled_horizontal:"bg3col.png"
                background_horizontal:"bg3col.png"
                background_width:10
                on_value:setattr(root,"physical",self.value)
        Row:
            CLabel:
                text:"Focus"
            NumInput:
                id:focus
                on_text:setattr(root,"focus",self.text)
                text:root.focus
            CLabel:
                text:"Fitness"
            NumInput:
                id:fitness
                on_text:setattr(root,"fitness",self.text)
                text:root.fitness
            Widget:
            ToggleButton:
                text:"Unlock" if self.state=="down" else "Lock"
                state:"down"
                size_hint_y:None
                size_hint_x:None
                font_size:font_size
                height:font_size+row_padding*2
                font_name:"RobotoMono-Regular"
                ddoptions:["1","2","3"]
                width:3*font_size+row_padding*2
                id:edit_tickbox

                on_state:setattr(root,"edit_bio",self.state=="down")

                background_color:bg2col if self.state=="down" else h1col
                background_normal:""
                background_down:""
                color:fontcol
        Row:
            CLabel:
                text:"Strength"
            CLabel:
                fit:fitness.text if fitness.text else "0"
                text:"{:.1f}".format(int(self.fit)*(1+int(physical.value-3)/5))
            CLabel:
                text:"Speed"
            CLabel:
                fit:fitness.text if fitness.text else "0"

                text:"{:.1f}".format(int(self.fit)*(1-int(physical.value-3)/5))
        Row:
            AddAugButton:
                text:"+"
                on_release: root.add_aug_slot()
                disabled: type.text=="Human "
                background_color:1,1,1,1
                background_normal:"h1col.png"
                background_disabled_normal:"bg2col.png"
            Widget:
            CLabel:
                text:"Phage"
            CLabel:
                text:root.phage
                canvas.before:
                    Color:
                        rgba: h2col if float(self.text)>6 else h3col
                    Rectangle:
                        pos:self.pos
                        size:self.size
        ScrollView:
            do_scroll_x:False

            BoxLayout:
                orientation:"vertical"
                size_hint_y:None
                spacing:10
                height:sum(map(lambda a: a.height+self.spacing,self.children))
                id:eqbox

                Label:
                    text:str(root.equipment)

"""


class CButton(Button):
    pass


class DDButton(CButton):

    def showDropdown(self):
        self.dd = DropDown()
        for i in self.ddoptions:
            btn = CButton(text=i, size_hint_y=None, height=44, background_color=bg3col)
            btn.bind(on_release=lambda btn: self.dd.select(btn.text))
            self.dd.add_widget(btn)
        self.dd.bind(on_select=lambda instance, x: setattr(self, 'text', x))
        self.dd.open(self)


class Row(BoxLayout):
    pass


class Slot(Row):
    pass


class SepLine(Widget):
    pass


class AugSlot(Row):
    pass


class BigSlot(Slot):
    pass


class MedSlot(Slot):
    pass


class SmallSlot(Slot):
    pass


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

    equipment = ListProperty()
    augments = ListProperty()

    def __init__(self, **kwargs):
        super(CharScreen, self).__init__(**kwargs)


    def on_equipment(self, *a, **kw):
        self.fill_eq_box()

    def on_augments(self, *a, **kw):
        self.fill_eq_box()

    def fill_eq_box(self):
        for i in [i for i in self.eqbox.children]:
            self.eqbox.remove_widget(i)

        for i in self.augments:
            self.eqbox.add_widget(i)

        if self.augments:
            self.eqbox.add_widget(SepLine())

        for i in self.equipment:
            self.eqbox.add_widget(i)
        self.do_phage()

    def save(self):

        sd = {
            "cname": self.cname,
            "age": self.age,
            "fame": self.fame,
            "famename": self.famename,
            "type": self.type,
            "physical": self.physical,
            "focus": self.focus,
            "fitness": self.fitness,
            "augments": [],
            "equipment": []
        }

        for i in self.augments:
            d = {
                "description": i.description,
                "quality": i.quality,
                "titletext": i.titletext
            }

            sd["augments"].append(d)
        for i in self.equipment:
            d = {
                "description": i.description,
                "quality": i.quality,
                "titletext": i.titletext
            }

            sd["equipment"].append(d)
        print(sd["equipment"])
        print(sd["augments"])
        with open("save.json", "w") as file:
            json.dump(sd, file)

    def add_aug_slot(self):
        bs = AugSlot()
        bs.titletext = "Augment"
        self.augments.append(bs)

    def do_phage(self):
        a = 0.0

        for i in self.augments:
            if i.quality == "":
                continue
            a += 10 - int(i.quality)

        self.phage = str(a)

    def load(self,*_):
        if exists("save.json"):
            with open("save.json", "r") as file:
                l = json.load(file)

            eq = l.pop("equipment")

            ag = l.pop("augments")

            for i in l:
                setattr(self, i, l[i])

            for augment_dict in ag:
                slot=AugSlot()
                self.augments.append(slot)
                for i in augment_dict:
                    setattr(slot,i,augment_dict[i])

            for equipment_dict in eq:
                if equipment_dict["titletext"]=="Small Weapon":
                    slot=SmallSlot()
                else:
                    slot=BigSlot()
                self.equipment.append(slot)

                for i in equipment_dict:
                    setattr(slot, i, equipment_dict[i])
        else:
            for i in range(2):
                a = BigSlot()
                a.titletext = "Big Weapon  "
                self.equipment.append(a)
            for i in range(4):
                a = SmallSlot()
                a.titletext = "Small Weapon"
                self.equipment.append(a)
            self.fill_eq_box()


class BlocksplorerApp(App):

    def build(self):
        Builder.load_string(SS)

        self.cs = CharScreen()
        Clock.schedule_once(self.cs.load, .1)

        return self.cs


if __name__ == "__main__":
    app = BlocksplorerApp()
    app.run()
    app.cs.save()
