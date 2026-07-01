from typing import Any
from app.game.interpreter.utils.variables import *

def validate(expr:str|None, variables:dict[str, Any]) -> bool:
    if expr is None: return True
    left,right, func = eval_conditional_expression(expr)
    if "${" in left: left = get_clean_left_and_right(left, variables)
    if "${" in right: right = get_clean_left_and_right(right, variables)
    result = func(parse_variable_value(left.strip()), parse_variable_value(right.strip()))
    if not result:
        print(f'expr: {expr}, {left}, {right} --> {result}')
    return result
    
def get_clean_left_and_right(expr:str, variables: dict[str,Any]) -> str:
    return interpolate_variables_in_text_line(expr=expr, variables=variables)