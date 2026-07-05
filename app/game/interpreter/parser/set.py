import ast
from typing import Any

from app.game.interpreter.models import SetNode
from app.game.interpreter.utils.variables import prepare_set_expression, interpolate_variables_in_text_line
from app.game.interpreter.utils.expressions import build_expression_tree

def parse_set_node(line: str, pointer: int, variables:dict[str, Any]) -> SetNode:
    # #set set_test = ${set_test} - 1
    var, expr = prepare_set_expression(line, variables)
    expr = interpolate_variables_in_text_line(expr, variables)
    expr_tree = build_expression_tree(ast.parse(expr, mode="eval"))
    node = SetNode(pointer, var, expr_tree)

    return node