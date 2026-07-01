from typing import Any
from pathlib import Path

from app.game.interpreter.models import Node, TextNode
from app.game.interpreter.parser.bookmark import parse_bookmark
from app.game.interpreter.parser.choice import parse_choice_node
from app.game.interpreter.utils.variables import interpolate_variables_in_text_line
from app.game.interpreter.parser.conditional import parse_conditional_node

class Parser:
    def __init__(self, variables: dict[str,Any], path:Path) -> None:
        self.variables = variables
        self.file_path = path
    
    def parse(self, lines:list[str]) -> list[Node]:
        nodes = []
        pointer = 0
        
        while pointer < len(lines):
            node, pointer = self.parse_node(lines, pointer)
            
            if node is not None:
                nodes.append(node)
        
        return nodes
    
    def parse_node(self, lines: list[str], pointer:int) -> tuple[Node | None, int]:
        line = lines[pointer]
        clean = line.strip()
        
        if clean.startswith('#bookmark'):
            bkmk = parse_bookmark(line, pointer, self.file_path)
            return bkmk, pointer+1
            
        if clean.startswith('#choice'):
            choice, pointer = parse_choice_node(self, lines, pointer)
            return choice, pointer
        
        if clean.startswith('#if'):
            conditional, pointer = parse_conditional_node(self, lines, pointer)
            return conditional, pointer
        
        # Text verification fallback
        if not clean.startswith(('*', '#')):
            text = interpolate_variables_in_text_line(line.strip(), self.variables)
            return TextNode(pointer, text), pointer+1
            
        return None, pointer + 1