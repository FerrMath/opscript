from typing import Any
from app.game.interpreter.models import ConditionBranch, Expression
from app.game.interpreter.utils.expressions import evaluate
from app.game.interpreter.utils.variables import *

def validate(node: ConditionBranch, variables:dict[str, Any]) -> bool:
    
    if node.condition is None:
        return True
    result = evaluate(node.condition, variables)
    return result
    
def get_clean_left_and_right(expr:str, variables: dict[str,Any]) -> str:
    return interpolate_variables_in_text_line(expr=expr, variables=variables)