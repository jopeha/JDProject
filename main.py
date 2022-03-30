import Generators
from Block import Block as BlockClass
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ListProperty,NumericProperty,StringProperty,ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.animation import Animation
from random import gauss
import threading
from kivy.clock import Clock
from kivy.utils import get_color_from_hex

SS="""
#:import utils kivy.utils
#:set hx utils.get_color_from_hex
#:set bg1col hx("#022436")
#:set bg2col hx("#012F46")
#:set fontcol hx("#EDF7D2")
#:set h1col hx("#842C2A")
#:set h2col hx("#c23D2A")
#:set h3col hx("#EA8A44")

<StartScreen>:
    name:"start"
    id:screen
    BoxLayout:
        orientation:"vertical"
        Button:
            text:"new"
            on_release:screen.new()
        Button:
            text:"load"
            
<LoadScreen>:

    id:screen
    progress:0
    text:"LOADSCREEN"
    BoxLayout:
        canvas:
            Color:
                rgba:bg1col
            Rectangle:
                pos:self.pos
                size:self.size
   
        orientation:"vertical"
        padding:100,0
        Widget:
        Label:
            canvas.before:
                Color:
                    rgba:bg2col
                Rectangle:
                    pos:self.pos
                    size:screen.progress*self.width,self.height
                Color:
                    rgba:h1col
                Line:
                    rectangle:self.pos+self.size
            size_hint:1,.1
            text:screen.text
            color:fontcol
            
        Widget:

<BlockScreen>:
    name:"block"
    done:False
    blockobj:blockobj
    id:screen
    
    BoxLayout:
        canvas:
            Color:
                rgba: bg1col
            Rectangle:
                size: self.size
    
        orientation:"vertical"
        BoxLayout:
            size_hint:1,.2
            orientation:"vertical"
            
        BoxLayout:

            orientation:"horizontal"

            BoxLayout:
                padding:20,20
                size_hint:.3,1
                Label:
                    halign:"left"
                    valign:"top"
                    text:screen.blockstats
                    text_size:self.size
                    size_hint_x:None
                    width:1920
                    markup:True
                    
        
                    
            BoxLayout:

                Block:
                    id:blockobj
                    progress:
                    block:screen.block
                
            BoxLayout:
                size_hint:.3,1
        BoxLayout:
            size_hint:1,.2

<Block>
    
    orientation:"vertical"

    

<BlockSection>:
    orientation:"horizontal"
    layerwidth:1
    id:section
    name:""
    color:1,1,1,1
    BoxLayout:
        size_hint_x:.25
        
    Button:
        canvas:
            Color:
                rgba:section.color
            Line:
                rectangle:self.pos+self.size
        size_hint_x:self.parent.layerwidth
        background_normal:""
        background_color:[1,1,1,.1] if self.state != "down" else [.5,.8,1,.2]
        background_down:""
        text:section.name
    BoxLayout:
        size_hint_x:.25

<Sheet@Widget>
    canvas:
        Color:
            rgba:self.rgeb+[0.3]
        Rectangle:
            size:self.parent.size
    rgeb:[1,1,1]
    size_hint:0,0

"""

class StartScreen(Screen):
    pass


class LoadScreen(Screen):
    pass


class BlockScreen(Screen):
    block=ObjectProperty(BlockClass)
    blockstats=StringProperty("NOT LOADING")

    def make(self,**kw):
        self.block=Generators.block(**kw)
        self.blockobj.make()
        self.done=True
        self.blockstats=self.block.stats()


class BlockSection(BoxLayout):
    block=ObjectProperty(BlockClass)
    name=StringProperty("section")
    name=StringProperty("section")
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class Block(BoxLayout):

    layernum=NumericProperty(200)
    floors=NumericProperty()
    sections=ListProperty()
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

    def make(self):

        n=self.block.floors/len(self.block.shape)

        for pos,i in enumerate(self.block.shape):

            self.floors=(pos+1)*n

            bl=BlockSection(block=self.block,name=f"{len(self.block.shape)-pos}")#,section=Section())



            bl.layerwidth=i
            self.add_widget(bl)
            self.sections.append(bl)

class BlocksplorerApp(App):
    loading=False
    _progress=0,"SHIT"

    @property
    def progress(self):
        return self._progress

    @progress.setter
    def progress(self,value):
        self._progress=value


    def build(self):
        self.sm = ScreenManager()
        Builder.load_string(SS)

        self.ss,self.ls,self.bs=StartScreen(name="start"),LoadScreen(name="load"),BlockScreen(name="block")

        self.ss.new=self.start

        self.sm.add_widget(self.ss)
        self.sm.add_widget(self.ls)
        self.sm.add_widget(self.bs)

        return self.sm

    def back(self):
        if self.sm.current=="load" or self.sm.current=="block":
            self.sm.current="start"

    def start(self,**kwargs):
        self.sm.current="load"
        self.loadthread = threading.Thread(target=self.load)
        self.loadthread.start()
        self.caller=Clock.schedule_interval(self.tryloaded,.1)


    def load(self):
        self.loading=True
        self.bs.make(app=self)
        self.loading=False


    def tryloaded(self,*args):
        if not self.loading:
            self.loadthread.join()
            Clock.unschedule(self.caller)
            self.sm.current="block"

            return

        self.sm.current_screen.text=self._progress[1]
        self.sm.current_screen.progress=min(self._progress[0],1)







if __name__ == "__main__":
    app=BlocksplorerApp()
    app.run()
