from pathlib import Path
from typing import Any
from dataclasses import dataclass
from abc import ABC

@dataclass
class Node(ABC):
    position: int

class Expression:
    pass

@dataclass
class LiteralExpression(Expression):
    value: Any

@dataclass
class VariableExpression(Expression):
    name: str

@dataclass
class BinaryExpression(Expression):
    left: Expression
    right: Expression
    operator: str

@dataclass
class SetupData:
    meta:dict[str,str]
    variables:dict[str,Any]
    acts: list[str]

@dataclass
class FinishNode(Node):
    ...

@dataclass
class GotoData:
    target_name: str
    act_name: str | None

@dataclass
class ConditionBranch:
    condition: Expression | None
    children: list[Node]

@dataclass
class BookmarkNode(Node):
    act_path: Path
    name: str

@dataclass
class TextNode(Node):
    text: str
    
    def render(self):
        return self.text

@dataclass
class SetNode(Node):
    variable:str
    expression: Expression
    
    def eval(self):
        return ...

@dataclass
class OptionNode(Node):
    text: str
    children: list[Node]

@dataclass
class ChoiceNode(Node):
    options: list[OptionNode]

@dataclass
class ConditionNode(Node):
    branches: list[ConditionBranch]

@dataclass
class GotoNode(Node):
    target: GotoData