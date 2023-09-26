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
        self.input_box = InputBox(0,10,font_size*20,font_size+4,3,initial_word="> ")
    
    # process
    def _update(self):
        self.input_box.listen()
        
        if pyxel.btnp(pyxel.KEY_RETURN):
            print(self.input_box.get_text())
    
    # visualize
    def _draw(self):
        pyxel.cls(0)
        self.input_box.draw()