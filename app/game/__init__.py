from pathlib import Path

class Game:
    def __init__(self, game_folder:Path) -> None:
        self.__acts_folder = game_folder / 'acts'
    
    def setup(self):
        # Run the setup
        ...