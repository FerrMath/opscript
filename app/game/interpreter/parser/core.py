from typing import Any
from pathlib import Path

from app.game.interpreter.models import BookmarkNode, Node, TextNode
from app.game.interpreter.parser.bookmark import parse_bookmark
from app.game.interpreter.parser.choice import parse_choice_node
from app.game.interpreter.parser.set import parse_set_node
from app.game.interpreter.parser.conditional import parse_conditional_node
from app.game.interpreter.parser.goto import parse_goto_node

class Parser:
    def __init__(self, variables: dict[str,Any], path:Path) -> None:
        self.variables = variables
        self.file_path = path
    
    def parse(self, lines:list[str]) -> tuple[list[BookmarkNode],list[Node]]:
        nodes = []
        bookmarks = []
        pointer = 0
        
        while pointer < len(lines):
            
            node, pointer = self.parse_node(lines, pointer)
            if node is not None:
                if isinstance(node, BookmarkNode):
                    bookmarks.append(node)
                    continue
                nodes.append(node)

        return nodes, bookmarks
    
    def parse_bkmk(self, lines:list[str], position:int):
        line = lines[position]
        clean = line.strip()
        if clean.startswith('#bookmark'):
            bkmk, position = parse_bookmark(line, position, self.file_path)
            return bkmk, position +1
        return None, position + 1
    
    def parse_node(self, lines: list[str], pointer:int) -> tuple[Node | None, int]:
        line = lines[pointer]
        clean = line.strip()
        
        if clean.startswith('#goto'):
            goto = parse_goto_node(clean, pointer)
            return goto, pointer+1
    
        if clean.startswith('#set'):
            setter = parse_set_node(line, pointer, self.variables)
            return setter, pointer + 1
            
        if clean.startswith('#choice'):
            choice, pointer = parse_choice_node(self, lines, pointer)
            return choice, pointer
        
        if clean.startswith('#if'):
            conditional, pointer = parse_conditional_node(self, lines, pointer, self.variables)
            return conditional, pointer
        
        if clean.startswith('#bookmark'):
            bkmk, pointer = parse_bookmark(clean, pointer, self.file_path)
            return bkmk, pointer
        
        # Text verification fallback
        if not clean.startswith(('*', '#')):
            text = line.strip()
            return TextNode(pointer, text), pointer+1
            
        return None, pointer + 1