from app.game.interpreter.models import BookmarkNode
from pathlib import Path

def parse_bookmark(line: str, position:int, path:Path) -> BookmarkNode:
    try:
        name = line.split(maxsplit=1)[1]
    except IndexError:
        print(f"Error: no name for bookmark at file {path}\n Position -> {position}")
        raise
    
    return BookmarkNode(name=name, position=position, act_path=path)