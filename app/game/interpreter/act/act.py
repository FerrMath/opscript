from dataclasses import dataclass
from app.game.interpreter.models import TextNode, ChoiceNode, ConditionNode, Bookmark, Node

class Act:
    def __init__(self):
        self.nodes:list[Node] = []
        self.bookmarks = []
    
    def add_bookmark(self, bookmark: Bookmark):
        self.bookmarks.append(bookmark)
    
    def add_text_node(self, node: TextNode):
        self.nodes.append(node)
    
    def add_choice_node(self, node: ChoiceNode):
        self.nodes.append(node)
    
    def add_condition_node(self, node: ConditionNode):
        self.nodes.append(node)
        
    def get_all_nodes(self):
        return sorted(self.nodes, key=lambda e: e.position)
    
    def __str__(self) -> str:
        return (
            f"Act(bookmarks={len(self.bookmarks)}, "
            f"Conditional={[n for n in self.nodes if isinstance(n, ConditionNode)]}, "
            f"Choices={ [ n for n in self.nodes if isinstance(n, ChoiceNode)] },"
        )

    def __repr__(self) -> str:
        return (
            f"Act(bookmarks={self.bookmarks!r}, "
            f"Choices={ [ n for n in self.nodes if isinstance(n, ChoiceNode)] }"
        )