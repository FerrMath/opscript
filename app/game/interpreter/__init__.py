from pathlib import Path
from typing import Any
from dataclasses import dataclass

@dataclass
class SetupData:
    meta:dict[str,str]
    variables:dict[str,Any]
    acts: list[str]


class Interpreter:
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
    
    def is_ignorable_line(self, line:str) -> bool:
        """ Ignores empty lines and comment lines in the read file

        Args:
            line (str): Line being evaluated

        Returns:
            bool: True if the stripped line is empty or is marked as a comment in the txt file
        """
        return not line or line.startswith('//')

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