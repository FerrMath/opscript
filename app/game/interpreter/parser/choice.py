from app.game.interpreter.models import ChoiceNode, OptionNode
from app.game.interpreter.utils.text import get_indent
from app.game.interpreter.utils.variables import interpolate_variables_in_text_line

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.game.interpreter.parser.core import Parser

def parse_option_node(parser: "Parser", lines: list[str], pointer:int) -> tuple[OptionNode, int]:
    line = lines[pointer]
    clean = line.strip()
    try:
        text = interpolate_variables_in_text_line(clean.split(maxsplit=1)[1], parser.variables)
    except IndexError as e:
        raise ValueError(
            f'Option needs to have a description: line {pointer}'
        )
    
    option = OptionNode(pointer, text, [])
    
    base_indent = get_indent(line)
    pointer += 1
    
    while pointer < len(lines):
        line = lines[pointer]
        clean = line.strip()
        
        current_indent = get_indent(line)
        
        if current_indent <= base_indent:
            break
        
        if clean.startswith('*option'):
            raise ValueError(f'Option cannot contain another option directly: line {pointer}')
        
        child, pointer = parser.parse_node(lines, pointer)
        if child:
            option.children.append(child)
    return option, pointer

def parse_choice_node(parser: "Parser", lines:list[str], pointer:int) -> tuple[ChoiceNode|None, int]:
    choice = ChoiceNode(pointer, [])
    base_indent = get_indent(lines[pointer])
    pointer += 1
    
    while pointer < len(lines):
        line = lines[pointer]
        current_indent = get_indent(line)
        clean_line = line.strip()
        
        if current_indent <= base_indent:
            break
        
        if clean_line.startswith("*option"):
            option, pointer = parse_option_node(parser, lines, pointer)
            choice.options.append(option)
            continue
        
        raise ValueError(f'Choice só pode conter options: line {pointer} -> {line}')
    
    return choice, pointer