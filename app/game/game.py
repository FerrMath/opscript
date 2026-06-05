from typing import Any
from pathlib import Path
from app.game.interpreter import Interpreter
from app.game.interpreter.act import Act

class Game:
    def __init__(self, game_folder:Path) -> None:
        self.__acts_folder:Path = game_folder / 'acts'
        self.__interpreter:Interpreter = Interpreter(self.__acts_folder)
        self.meta:dict[str,str] = {}
        self.variables:dict[str,Any] = {}
        self.acts: list[Act] = [] # Temp will create Act class later
    
    def setup(self):
        # Get the meta and variables data
        data = self.__interpreter.parse_setup()
        self.meta = data.meta
        self.variables = data.variables
        
        # prepare the acts data
        act_names = data.acts
        for act in act_names:
            act_path = self.__acts_folder / f'{act}.txt'
            self.acts.append(self.__interpreter.parse_act(act_path, self.variables))