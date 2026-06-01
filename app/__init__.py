from app.game import Game
from pathlib import Path

def create_new_app(updated_path:Path | None = None):
    DEFAULT_FOLDER = Path('./test_game_folder')
    return Game(updated_path or DEFAULT_FOLDER)