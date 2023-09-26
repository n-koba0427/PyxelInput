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
        self.input_box = InputBox(self.writer,0,0,font_size*20,font_size+4,font=params.FONT,initial_word="$ ")
        
        self.output_text_list = []
    
    # process
    def _update(self):
        self.input_box.listen()
        
        if pyxel.btnp(pyxel.KEY_RETURN):
            cmd = self.input_box.get_text()
            self.output_text_list = []
            for output_text in run_command(cmd).split("\n"):
                self.output_text_list.append(output_text)
    
    # visualize
    def _draw(self):
        pyxel.cls(0)
        self.input_box.draw()
        
        font_size = self.params.FONT_SIZE
        
        for i, output_text in enumerate(self.output_text_list):
            if len(output_text)>0:
                self.writer.draw(
                    x=0,
                    y=(font_size+4)*(i+2),
                    text=output_text,
                    font_size=font_size,
                    font_color=7,
                )