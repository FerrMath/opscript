import re
import operator
from typing import Any, Callable

VAR_PATTERN = re.compile(r"\$\{([^}]+)\}")

def interpolate_variables_in_text_line(expr: str, variables: dict[str, Any])-> str:
    def repl(match):
        var_name = match.group(1)
        var = variables.get(var_name)
        if var is None:
            raise ValueError(f'Variable "{var_name}" is not defined, valid variables: {variables}')
        return str(var)
    return VAR_PATTERN.sub(repl, expr)

def parse_variable_value(value: str) -> Any:
        temp_value = value.lower().strip()
        
        # List
        if temp_value.startswith('[') and temp_value.endswith(']'):
            items = value.strip()[1:-1].split(',')
            return [parse_variable_value(i.strip()) for i in items]
        
        # Boolean
        if temp_value == "true": 
            return True
        if temp_value == "false": 
            return False
        
        # Int
        try:
            return int(value)
        except ValueError:
            pass
        
        # Float
        try:
            return float(value)
        except ValueError:
            pass
        
        # Default / Str
        return value.replace("'", "").replace('"', "")
    
def eval_conditional_expression(expr:str) -> tuple[str,str, Callable]:
    ops = {
        "==": operator.eq,
        "!=": operator.ne,
        ">": operator.gt,
        "<": operator.lt,
        ">=": operator.ge,
        "<=": operator.le,
    }

    for op_str, op_func in ops.items():
        if op_str in expr:
            left, right = expr.split(op_str)
            return left, right, op_func
    raise ValueError