import pyxel
from .utils import *

from .pyxel_input import InputBox
import PyxelUniversalFont as puf

class Params:
    WINDOW_SIZE = (400,300)
    SOURCE = get_data_path("data/img.pyxres")
    FONT_SIZE = 16
    FONT = "misaki_gothic.ttf"

class App:
    def __init__(self, params:Params) -> None:
        # initialize window
        self.WINDOW_WIDTH, self.WINDOW_HEIGHT = params.WINDOW_SIZE
        pyxel.init(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        
        # load data
        pyxel.load(params.SOURCE)
        
        # initialize variables
        self._reset(params)
        
        # run app
        pyxel.run(self._update, self._draw)
    
    # initialize variables
    def _reset(self, params:Params):
        self.params = params
        self.writer = puf.Writer(params.FONT)
        
        font_size = params.FONT_SIZE

        self.input_box = InputBox(
            x=10,
            y=10,
            w=font_size*20,
            h=font_size+4,
            text_color=0,
            background_color=13,
            border_color=0,
            margin=2,
            indicator=True,
            font=params.FONT,
            initial_word="> "
        )
        self.text_list = list()
    
    # process
    def _update(self):
        self.input_box.listen()
        
        if pyxel.btnp(pyxel.KEY_RETURN):
            self.text_list.append(self.input_box.get_text())
            self.input_box.clear()
    
    # visualize
    def _draw(self):
        pyxel.cls(7)
        self.input_box.draw()
        
        font_size = self.params.FONT_SIZE
        for i,text in enumerate(self.text_list):
            self.writer.draw(10,font_size*(i+2)+10,text,font_size,16)