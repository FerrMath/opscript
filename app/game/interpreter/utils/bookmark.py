from app.game.interpreter.act import Act
from app.game.interpreter.models import BookmarkNode, GotoData


def find_bookmark_in_act(data: GotoData, act:Act)-> BookmarkNode | None:
    return next((x for x in act.bookmarks if x.name == data.target_name), None)