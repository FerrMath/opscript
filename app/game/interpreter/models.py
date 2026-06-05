from pathlib import Path
from typing import Any
from dataclasses import dataclass

@dataclass
class SetupData:
    meta:dict[str,str]
    variables:dict[str,Any]
    acts: list[str]

@dataclass
class Bookmark:
    act_path: Path
    name: str
    position: int

@dataclass
class TextNode:
    text: str
    position: int