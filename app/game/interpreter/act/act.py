from dataclasses import dataclass
from app.game.interpreter.models import TextNode, ChoiceNode, Bookmark

class Act:
    def __init__(self):
        self.bookmarks: list[Bookmark] = []
        self.text_nodes: list[TextNode] = []
        self.choice_nodes: list[ChoiceNode] = []
    
    def add_bookmark(self, bookmark: Bookmark):
        self.bookmarks.append(bookmark)
    
    def add_text_node(self, node: TextNode):
        self.text_nodes.append(node)
    
    def add_choice_node(self, node: ChoiceNode):
        self.choice_nodes.append(node)
    
    def __str__(self) -> str:
        return (
            f"Act(bookmarks={len(self.bookmarks)}, "
            f"choices={len(self.choice_nodes)}, "
            f"text_nodes={len(self.text_nodes)})"
        )

    def __repr__(self) -> str:
        return (
            f"Act(bookmarks={self.bookmarks!r}, "
            f"choices={self.text_nodes!r}),"
            f"text_nodes={self.text_nodes!r})"
        )