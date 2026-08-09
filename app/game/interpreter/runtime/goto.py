from pathlib import Path

from app.game.interpreter.act import Act
from app.game.interpreter.models import BookmarkNode, GotoNode
from app.game.interpreter.utils.bookmark import find_bookmark_in_act


def get_bookmark_for_goto(goto:GotoNode, current_act:Act, acts:dict[Path,Act]) -> BookmarkNode:
    if goto.target.act_name is None or goto.target.act_name == current_act.name:
        bkmk = find_bookmark_in_act(goto.target, current_act)
        if not bkmk:
            raise ValueError(f"Bookmark '{goto.target.target_name}' not found in act '{current_act.name}' provided.")
        return bkmk
    
    target_act = next((act for act in acts.values() if act.name == goto.target.act_name), None)
    if target_act is None:
        raise ValueError("No valid act found to be targeted")
    
    bkmk = find_bookmark_in_act(goto.target, target_act)
    if not bkmk:
        raise ValueError(f"Bookmark '{goto.target.target_name}' not found in target act '{goto.target.act_name}'\n Valid bookmarks in {target_act.name} are: {target_act.bookmarks}")
    return bkmk
