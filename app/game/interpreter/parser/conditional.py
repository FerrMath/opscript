from app.game.interpreter.models import ConditionNode, ConditionBranch, Node
from app.game.interpreter.utils.text import get_clean_if_expression, get_indent
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.game.interpreter.parser.core import Parser

def parse_conditional_node(parser:"Parser", lines:list[str], pointer:int) -> tuple[ConditionNode | None, int]:
    node = ConditionNode(pointer, [])
    branch = ConditionBranch(get_clean_if_expression(lines[pointer]),children=[])
    
    base_indent = get_indent(lines[pointer])
    pointer += 1
    
    while pointer < len(lines):
        line = lines[pointer]
        clean = line.strip()
        current_indent = get_indent(line)
        
        if current_indent < base_indent:
            break
        
        if current_indent == base_indent:
            if clean.startswith('#elif'):
                node.branches.append(branch)
                branch = ConditionBranch(get_clean_if_expression(line), children=[])
                pointer +=1
                continue
            if clean.startswith("#else"):
                node.branches.append(branch)
                branch = ConditionBranch(None, children=[])
                pointer += 1
                continue
            break
        else:
            child, pointer = parser.parse_node(lines, pointer)
            if isinstance(child, Node):
                branch.children.append(child)
    node.branches.append(branch)
    return node, pointer