def is_ignorable_line(line: str) -> bool:
    return not line or line.startswith('//')

def get_indent(line:str) -> int:
    return len(line) - len(line.lstrip())

def get_clean_if_expression(line:str) -> str:
    return line.split(maxsplit=1)[1]