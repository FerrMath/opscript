from pathlib import Path
from app.game.interpreter import Interpreter

class Game:
    def __init__(self, game_folder:Path) -> None:
        self.__acts_folder = game_folder / 'acts'
        self.__interpreter = Interpreter(self.__acts_folder)
    
    def setup(self):
        # Run the setup
        data = self.__interpreter.parse_setup()
        print(data)
        ...