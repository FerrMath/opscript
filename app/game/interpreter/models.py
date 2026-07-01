from pathlib import Path
from typing import Any
from dataclasses import dataclass
from abc import ABC

@dataclass
class SetupData:
    meta:dict[str,str]
    variables:dict[str,Any]
    acts: list[str]

@dataclass
class ConditionBranch:
    condition: str | None
    children: list[Node]

@dataclass
class Node(ABC):
    position: int

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
class OptionNode(Node):
    text: str
    children: list[Node]

@dataclass
class ChoiceNode(Node):
    options: list[OptionNode]

@dataclass
class ConditionNode(Node):
    branches: list[ConditionBranch]