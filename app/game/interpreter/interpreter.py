import re
from pathlib import Path
from typing import Any
from app.game.interpreter.act import Act
from app.game.interpreter.models import SetupData, TextNode, Bookmark, ChoiceNode, OptionNode, Node

class Interpreter:
    VAR_PATTERN = re.compile(r"\$\{([^}]+)\}")
    
    def __init__(self, game_folder: Path):
        self.setupfile = game_folder / 'setup.txt'

    def parse_setup(self) -> SetupData:
        """Handles parsing of the necessary setup for the game\n
        
        Runs the interpreter on the file setup.txt found inside the .../game_folder/acts folder,
        handling the gathering of meta data, the variables that will be used in the game, and the act names

        Returns:
            SetupData: Custom data type with the meta, variable and acts data
        """
        meta: dict[str, str] = {}
        variables: dict[str, Any] = {}
        acts: list[str] = []
        
        with open(self.setupfile, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                
                if self.is_ignorable_line(line): 
                    continue
                
                # Meta data gathering
                try:
                    if line.startswith('#title'):
                        meta['title'] = line.split(maxsplit=1)[1]
                        continue
                    if line.startswith('#author'):
                        meta['author'] = line.split(maxsplit=1)[1]
                        continue
                except IndexError as e:
                    print(f'Error at line: "{line}" invalid meta data @ startup.txt')
                    raise e
                
                # Variables
                try:
                    if line.startswith('#variable'):
                        _, name, value = line.split(maxsplit=2)
                        if name in variables:
                            raise ValueError(f'Variable "{name}" already exists')
                        variables[name] = self.parse_variable_value(value)
                        continue
                except IndexError as e:
                    print(f'Error at line: "{line}" invalid Variable data @ startup.txt: invalid variable declaration')
                    raise e
                except ValueError as e:
                    print(f'Error at line: "{line}" invalid variable data @ startup.txt: variable already defined')
                    raise e

                # Acts
                try:
                    if line.startswith('#acts'):
                        raw_acts = line.split(maxsplit=1)[1]
                        acts = self.parse_variable_value(raw_acts)
                        continue
                except IndexError as e:
                    print(f'Error at line: "{line}" invalid act data @ startup.txt: No act name added to acts list')
                    raise e
                except Exception as e:
                    raise e
        return SetupData(meta=meta, variables=variables, acts=acts)

    def parse_act(self, act_path: Path, variables: dict[str, Any]) -> Act:
        """Parses an act file.

        Args:
            act_path (Path): Path to the act file.
            variables (dict[str, Any]): Variables available during parsing.

        Raises:
            FileNotFoundError: If the act file cannot be found.

        Returns:
            dict[str, Any]: TEMP Parsed act data.
        """
        if not act_path.exists():
            raise FileNotFoundError(
                f'Act at path {act_path} does not exist, make sure to have the file created inside of the folder "Acts"'
            )
        
        with open(act_path, 'r', encoding='utf-8') as file:
            act = Act()
            pointer = 0
            # Clean and filter lines safely
            lines: list[str] = [line.rstrip() for line in file if not self.is_ignorable_line(line.strip())]
            
            while pointer < len(lines):
                line = lines[pointer]
                # Reassign pointer based on where _process_line finishes reading
                pointer = self._process_line(line, pointer, variables, lines, act, act_path)
        return act

    def _process_line(self, line: str, pointer: int, variables: dict[str, Any], lines: list[str], current_act: Act, act_path: Path) -> int:
        
        if line.startswith('#bookmark'):
            bkm = self.parse_bookmark(line, pointer, act_path)
            current_act.add_bookmark(bkm)
            return pointer + 1
            
        if line.startswith('#choice'):
            choice, updatedPointer = self.parse_choice_node(lines, pointer, variables)
            current_act.add_choice_node(choice)
            return updatedPointer
            
        # Text verification fallback
        if not line.startswith(('*', '#')):
            node = self.parse_text_node(line, pointer, variables)
            current_act.add_text_node(node)
            return pointer + 1
            
        return pointer + 1

    def is_ignorable_line(self, line: str) -> bool:
        """ Ignores empty lines and comment lines in the read file

        Args:
            line (str): Line being evaluated

        Returns:
            bool: True if the stripped line is empty or is marked as a comment in the txt file
        """
        return not line or line.startswith('//')

    def parse_text_node(self, line: str, pointer: int, variables: dict[str, Any]) -> TextNode:
        node = TextNode(text=line, position=pointer)
        if '${' in line:
            text = self.interpolate_variables_in_text_line(line, variables)
            node.text = text
        return node

    def parse_option_node(self, lines:list[str], pointer:int, variables: dict[str,Any]) -> tuple[OptionNode, int]:
        line = lines[pointer]
        clean = line.strip()
        try:
            txt = self.interpolate_variables_in_text_line(clean.split(maxsplit=1)[1], variables)
        except IndexError:
            raise ValueError(
                f'Option needs to have a description: line {pointer}'
            )

        option = OptionNode(pointer, txt, [])
        
        base_indent = self.get_indent(line)
        updatedPointer = pointer + 1
        
        while updatedPointer < len(lines):
            line = lines[updatedPointer]
            clean = line.strip()
            
            current_indent = self.get_indent(line)
            
            if current_indent <= base_indent:
                break
            
            if clean.startswith('#choice'):
                choice, updatedPointer = self.parse_choice_node(lines, updatedPointer, variables)
                option.children.append(choice)
                continue
            
            elif clean.startswith('*option'):
                raise ValueError(
                    f'Option cannot contain another option directly: line {updatedPointer}'
                )
            
            option.children.append(
                TextNode(text=clean, position=updatedPointer)
            )
            updatedPointer += 1
        return option, updatedPointer
    
    def parse_choice_node(self, lines:list[str], pointer:int, variables: dict[str,Any])-> tuple[ChoiceNode, int]:
        choice = ChoiceNode(pointer, [])
        base_indent = self.get_indent(lines[pointer])
        updatedPointer = pointer + 1
        
        while updatedPointer < len(lines):
            line = lines[updatedPointer]
            current_indent = self.get_indent(line)
            clean_line = line.strip()
            if current_indent <= base_indent:
                break
            if clean_line.startswith('*option'):
                option, updatedPointer = self.parse_option_node(lines, updatedPointer, variables)
                choice.options.append(option)
                continue
            raise ValueError(f'Choice só pode conter options: line {updatedPointer} -> {line}')
        return choice, updatedPointer
        
    def parse_bookmark(self, line: str, pointer: int, act_path: Path) -> Bookmark:
        mark = line.split(maxsplit=1)[1]
        return Bookmark(act_path, mark, pointer)

    def get_indent(self, line:str) -> int:
        return len(line) - len(line.lstrip())

    def interpolate_variables_in_text_line(self, expr: str, variables: dict) -> str:
        def repl(match):
            var_name = match.group(1)
            var = variables.get(var_name)
            if var is None:
                raise ValueError(f'Variable "{var_name}" is not defined')
            return str(var)
        return self.VAR_PATTERN.sub(repl, expr)

    def parse_variable_value(self, value: str) -> Any:
        temp_value = value.lower().strip()
        
        # List
        if temp_value.startswith('[') and temp_value.endswith(']'):
            items = value.strip()[1:-1].split(',')
            return [self.parse_variable_value(i.strip()) for i in items]
        
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