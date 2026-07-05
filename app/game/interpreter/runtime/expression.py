from app.game.interpreter.models import Expression
from app.game.interpreter.utils.expressions import evaluate
from typing import Any

def eval(expr:Expression, variables:dict[str, Any]) -> Any:
    return evaluate(expr, variables)
