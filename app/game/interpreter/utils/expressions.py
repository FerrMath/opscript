import ast
import operator

from app.game.interpreter.models import Expression, BinaryExpression, LiteralExpression, VariableExpression
from typing import Any

def build_expression_tree(node: ast.AST) -> Expression:
    
    if isinstance(node, ast.Expression):
        return build_expression_tree(node.body)
    
    if isinstance(node, ast.BinOp):
        ops = {ast.Add:'+', ast.Sub:'-', ast.Mult: '*', ast.Div: '/'}
        return BinaryExpression(left = build_expression_tree(node.left), right=build_expression_tree(node.right), operator=ops[type(node.op)])
    
    if isinstance(node, ast.Compare):
        compare_ops = {
            ast.Gt: '>', ast.Lt: '<', ast.GtE: '>=', 
            ast.LtE: '<=', ast.Eq: '==', ast.NotEq: '!='
        }
        return BinaryExpression(left=build_expression_tree(node.left), right=build_expression_tree(node.comparators[0]), operator=compare_ops[type(node.ops[0])])
    
    elif isinstance(node, ast.Constant):
        return LiteralExpression(node.value)
    
    elif isinstance(node, ast.Name):
        return VariableExpression(node.id)
    
    raise ValueError("Unsuported node type")

def evaluate(expr:Expression, variables:dict) -> Any:
    if isinstance(expr, LiteralExpression):
        return expr.value
    
    if isinstance(expr, VariableExpression):
        if expr.name in variables:
            return variables[expr.name]
        else:
            # Fallback if writer didn't add quotes to symbolize a string in the original file
            return expr.name
    
    if isinstance(expr, BinaryExpression):
        left_val = evaluate(expr.left, variables)
        right_val = evaluate(expr.right, variables)
        
        if isinstance(left_val, str) or isinstance(right_val, str):
            if expr.operator not in ['==','!=']:
                raise TypeError(f"Strings cannot be used with operator {expr.operator}. Only numbers allowed")
            
        
        operations = {
            '+': operator.add, '-': operator.sub, 
            '*': operator.mul, '/': operator.truediv,
            '>': operator.gt,  '<': operator.lt,
            '>=': operator.ge, '<=': operator.le,
            '==': operator.eq, '!=': operator.ne
        }
        return operations[expr.operator](left_val, right_val)