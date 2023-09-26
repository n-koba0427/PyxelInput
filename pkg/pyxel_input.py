import pyxel
import PyxelUniversalFont as puf
from .utils import *

from pynput import keyboard

class Manager:
    def __init__(self) -> None:
        self.lib = {}
        self.latest_id = -1
    
    def get_id(self, obj):
        self.latest_id += 1
        self.lib[self.latest_id] = obj
        return self.latest_id
    
    def deactivate_all(self):
        for obj in self.lib.values():
            obj.stop_listen()
    
manager = Manager()

class InputBox:
    def __init__(
            self,
            x:int, y:int, w:int, h:int,
            text_color=7,
            background_color=-1,
            border_color=-1,
            margin = 2,
            indicator=True,
            font="misaki_gothic.ttf",
            initial_word=""
        ) -> None:
        
        self.x, self.y, self.w, self.h = x, y, w, h
        self.text_color = text_color
        self.background_color = background_color
        self.border_color = border_color
        self.margin = margin
        self.indicator = indicator
        self.writer = puf.Writer(font)
        self.initial_word = initial_word
        
        self._reset()
        
    def _reset(self):
        self.text = self.initial_word+" "
        self.position = len(self.initial_word)
        self.current_key = None
        self.shift_pressed = False
        self.listener = keyboard.Listener(on_press=self._on_press, on_release=self._on_release)
        self.active = False
        self.id = manager.get_id(self)
        self._quit_customize()
        
    def _on_press(self, key):
        if key == keyboard.Key.shift:
            self.shift_pressed = True
        elif hasattr(key, 'char') and key.char:
            self.current_key = key.char.upper() if self.shift_pressed else key.char

    def _on_release(self, key):
        if key == keyboard.Key.shift:
            self.shift_pressed = False
            
    def _add_text(self, character):
        self.text = self.text[:-1]
        self.text = self.text[:self.position] + character + self.text[self.position:]+" "
        self.position += 1
            
    def _remove_text(self, time=1):
        if time < 0:
            time = len(self.get_text())
        for _ in range(time):
            if self.position > len(self.initial_word):
                self.text = self.text[:self.position-1] + self.text[self.position:]
                self.position -= 1
    
    def clear(self):
        self._remove_text(-1)
    
    def _mask_string(self, s, index):
        index = int(index)
        masked = [' '] * len(s)
        if 0 <= index < len(s):
            masked[index] = "_"
        return ''.join(masked)
    
    def _quit_customize(self):
        original_quit = pyxel.quit
        def custom_quit():
            self.stop_listen()
            original_quit()
        pyxel.quit = custom_quit
            
    def listen(self):
        if not self.active:
            manager.deactivate_all()
            self.listener.start()
            self.active = True
            
        if pyxel.btnp(pyxel.KEY_SPACE):
            self._add_text(" ")
        
        if self.current_key:
            self._add_text(self.current_key)
            self.current_key = None
            
        if pyxel.btnp(pyxel.KEY_BACKSPACE):
            self._remove_text()
            
        if pyxel.btnp(pyxel.KEY_LEFT):
            if self.position > len(self.initial_word):
                self.position -= 1
        
        if pyxel.btnp(pyxel.KEY_RIGHT):
            if self.position < len(self.text)-1:
                self.position += 1
    
    def stop_listen(self):
        self.listener.stop()
        self.active = False
    
    def draw(self):
        if self.background_color >= 0:
            pyxel.rect(
                x=self.x,
                y=self.y,
                w=self.w,
                h=self.h,
                col=self.background_color,
            )
        if self.border_color >= 0:
            pyxel.rectb(
                x=self.x,
                y=self.y,
                w=self.w,
                h=self.h,
                col=self.border_color,
            )
        
        self.writer.draw(
            x=self.x+self.margin,
            y=self.y+self.margin,
            text=self.text,
            font_size=self.h-(self.margin*2),
            font_color=self.text_color,
            background_color=-1,
        )
        if self.indicator:
            self.writer.draw(
                x=self.x+self.margin,
                y=self.y+self.margin+1,
                text=self._mask_string(self.text, self.position),
                font_size=self.h-(self.margin*2),
                font_color=self.text_color,
                background_color=-1,
            )
        
    def get_text(self):
        return self.text[len(self.initial_word):-1]