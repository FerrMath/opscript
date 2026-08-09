from app.game.interpreter.models import GotoData

def is_ignorable_line(line: str) -> bool:
    return not line or line.startswith('//')

def get_indent(line:str) -> int:
    return len(line) - len(line.lstrip())

def get_clean_expression(line:str) -> str:
    return line.split(maxsplit=1)[1]

def get_clean_goto(line:str) -> GotoData:
    try:
        _,act_name, target_name = line.split(maxsplit=2)
    except IndexError:
        _, target_name = line.split(maxsplit=1)
        act_name = None
    return GotoData(target_name, act_name)