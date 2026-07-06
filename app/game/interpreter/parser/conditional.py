import ast

from app.game.interpreter.models import ConditionNode, ConditionBranch, Node
from app.game.interpreter.utils.expressions import build_expression_tree, create_clean_ast_node
from app.game.interpreter.utils.text import get_indent
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from app.game.interpreter.parser.core import Parser

def parse_conditional_node(parser:"Parser", lines:list[str], pointer:int, variables:dict[str,Any]) -> tuple[ConditionNode | None, int]:
    node = ConditionNode(pointer, [])
    expr = create_clean_ast_node(lines[pointer], variables)
    branch = ConditionBranch(build_expression_tree(expr), children=[])
    
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
                expr = create_clean_ast_node(lines[pointer], variables)
                branch = ConditionBranch(build_expression_tree(expr), children=[])
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