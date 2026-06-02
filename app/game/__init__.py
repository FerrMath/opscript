from typing import Any
from pathlib import Path
from app.game.interpreter import Interpreter

class Game:
    def __init__(self, game_folder:Path) -> None:
        self.__acts_folder:Path = game_folder / 'acts'
        self.__interpreter:Interpreter = Interpreter(self.__acts_folder)
        self.meta:dict[str,str] = {}
        self.variables:dict[str,Any] = {}
        self.acts: list[str] = [] # Temp will create Act class later
    
    def setup(self):
        # Run the setup
        data = self.__interpreter.parse_setup()
        self.meta = data.meta
        self.variables = data.variables
        self.acts = data.acts
