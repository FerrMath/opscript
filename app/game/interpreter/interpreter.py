from pathlib import Path
from typing import Any
from app.game.interpreter.act import Act
from app.game.interpreter.parser.core import Parser
from app.game.interpreter.utils.text import is_ignorable_line
from app.game.interpreter.utils.variables import parse_variable_value
from app.game.interpreter.models import SetupData

class Interpreter:
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
                
                if is_ignorable_line(line): 
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
                    if line.startswith('#var'):
                        _, name, value = line.split(maxsplit=2)
                        if name in variables:
                            raise ValueError(f'Variable "{name}" already exists')
                        variables[name] = parse_variable_value(value)
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
                        acts = parse_variable_value(raw_acts)
                        continue
                except IndexError as e:
                    print(f'Error at line: "{line}" invalid act data @ startup.txt: No act name added to acts list')
                    raise e
                except Exception as e:
                    raise e
        return SetupData(meta=meta, variables=variables, acts=acts)

    def parse_act(self, act_name:str, act_path: Path, variables: dict[str, Any]) -> Act:
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
            # Clean and filter lines safely
            lines: list[str] = [line.rstrip() for line in file if not is_ignorable_line(line.strip())]

        act = Act(act_name, act_path)
        parser = Parser(variables, act_path)
        nodes = parser.parse(lines)
        
        for node in nodes:
            act.nodes.append(node)
            
        return act
