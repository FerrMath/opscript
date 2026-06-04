import re
from pathlib import Path
from typing import Any
from dataclasses import dataclass

@dataclass
class SetupData:
    meta:dict[str,str]
    variables:dict[str,Any]
    acts: list[str]


class Interpreter:
    VAR_PATTERN = re.compile(r"\$\{([^}]+)\}")
    
    def __init__(self, game_folder:Path):
        self.setupfile = game_folder / 'setup.txt'

    def parse_setup(self) -> SetupData:
        """Handles parsing of the necessary setup for the game\n
        
        Runs the interpreter on the file setup.txt found inside the .../game_folder/acts folder,
        handling the gathering of meta data, the variables that will be used in the game, and the act names

        Returns:
            SetupData: Custom data type with the meta, variable and acts data
        """
        
        meta:dict[str,str] = {}
        variables:dict[str,Any] = {}
        acts:list[str] = []
        
        with open(self.setupfile, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                
                if self.is_ignorable_line(line): continue
                
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
                        # TODO will parse the [] captured in the raw_acts into a real python list
                        acts = self.parse_variable_value(raw_acts)
                        continue
                except IndexError as e:
                    print(f'Error at line: "{line}" invalid act data @ startup.txt: No act name added to acts list')
                    raise e
                except Exception as e:
                    raise e
        return SetupData(meta=meta, variables=variables, acts=acts)

    def parse_act(self, act_path: Path, variables: dict[str, Any]) -> dict[str, Any]:
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
        
        with open(act_path,'r',encoding='utf-8') as file:
            data = {'text':[],'bookmarks':[]} #Temp
            pointer = 0
            lines: list[str] = [line.strip() for line in file if not self.is_ignorable_line(line.strip())]
            while pointer < len(lines):
                line = lines[pointer]
                
                # Get the bookmarks
                if line.startswith('#bookmark'):
                    try:
                        mark = line.split(maxsplit=1)[1]
                        data['bookmarks'].append({'bookmark':mark, 'position':pointer})
                        pointer += 1
                        continue
                    except IndexError as e:
                        raise e
                
                # Get the raw text with variables
                if not line.startswith(('*','#')): # TEMP
                    if '${' in line:
                        line = self.parse_text_line(line, variables)
                    data['text'].append(line)
                    pointer +=1
                    continue
                pointer +=1
        return data

    def is_ignorable_line(self, line:str) -> bool:
        """ Ignores empty lines and comment lines in the read file

        Args:
            line (str): Line being evaluated

        Returns:
            bool: True if the stripped line is empty or is marked as a comment in the txt file
        """
        return not line or line.startswith('//')

    def parse_text_line(self, expr:str, variables: dict) -> str:
        def repl(match):
            var_name = match.group(1)
            var = variables.get(var_name)
            if var is None:
                raise ValueError(f'Variable "{var_name}" is not defined')
            return str(var)
        return self.VAR_PATTERN.sub(repl, expr)

    def parse_variable_value(self, value:str) -> Any:
        temp_value = value.lower().strip()
        
        # List
        if temp_value.startswith('[') and temp_value.endswith(']'):
            items = value.strip()[1:-1].split(',')
            items = [self.parse_variable_value(i.strip()) for i in items]
            return items
        
        # boolean
        if value == "true" : return True
        if value == "false": return False
        
        # Int
        try:
            return int(value)
        except ValueError as e:
            pass
        
        # Float
        try:
            return float(value)
        except ValueError as e:
            pass
        
        # Default / Str
        return value.replace("'", "").replace('"',"")