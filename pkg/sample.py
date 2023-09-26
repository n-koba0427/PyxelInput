import pyxel
from .utils import *

from .pyxel_input import InputBox

class Params:
    WINDOW_SIZE = (400,300)
    SOURCE = get_data_path("data/img.pyxres")
    FONT_SIZE = 16

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
        
        font_size = params.FONT_SIZE
        self.input_box_black = InputBox(10,10,font_size*20,font_size+4,3)
        self.input_box_white = InputBox(10,40,font_size*20,font_size+4,0,7,1)
        
        self.flag = True
    
    # process
    def _update(self):
        if self.flag:
            self.input_box_black.listen()
        else:
            self.input_box_white.listen()
        
        if pyxel.btnp(pyxel.KEY_RETURN):
            print(self.input_box_black.get_text())
            print(self.input_box_white.get_text())
            
        if pyxel.btnp(pyxel.KEY_TAB):
            self.flag = not self.flag
    
    # visualize
    def _draw(self):
        self.input_box_black.draw()
        self.input_box_white.draw()