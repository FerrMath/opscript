from pathlib import Path
from app.game.interpreter.models import GotoNode, GotoData

ACT_FOLDER_PATH = Path("./test_game_folder/acts")

def parse_goto_node(line:str, postion:int) -> GotoNode:
    try:
        _, act_name, target_name = line.split(maxsplit=2)
    except:
        _, target_name = line.split(maxsplit=1)
        act_name = None
    data = GotoData(target_name, act_name)
    return GotoNode(postion, data)