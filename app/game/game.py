from typing import Any
from pathlib import Path
from app.game.interpreter import Interpreter
from app.game.interpreter.act import Act
from app.game.interpreter.models import *
from app.game.interpreter.runtime.conditions import validate
from app.game.interpreter.runtime.expression import eval
from app.game.interpreter.runtime.goto import get_bookmark_for_goto
from app.game.interpreter.runtime.text import get_interpolated_text_line

class Game:
    def __init__(self, game_folder:Path) -> None:
        self.__acts_folder:Path = game_folder / 'acts'
        self.__interpreter:Interpreter = Interpreter(self.__acts_folder)
        self.meta:dict[str,str] = {}
        self.variables:dict[str,Any] = {}
        self.acts: dict[Path,Act] = {} # Temp will create Act class later
    
    def setup(self):
        # Get the meta and variables data
        data = self.__interpreter.parse_setup()
        self.meta = data.meta
        self.variables = data.variables
        
        # prepare the acts data as a dict {'act/path/': ActObject}
        self.acts = {
            self.__acts_folder/f"{act}.txt"
            :self.__interpreter.parse_act(act, self.__acts_folder/f"{act}.txt", self.variables)
            for act in data.acts
        }
    
    def run(self):
        if not self.acts:
            raise ValueError("The game has no acts")
        acts = list(self.acts.values())
        current_act_index = 0
        current_act = acts[current_act_index]
        node_index = 0
        game_running = True
        while game_running:
            if node_index >= len(current_act.nodes):
                current_act_index += 1

                if current_act_index >= len(acts):
                    print("\n\n\n The end \n\n\n")
                    return

                current_act = acts[current_act_index]
                node_index = 0
                continue
            
            current_node = current_act.nodes[node_index]
            special_node = self.render_node(current_node, current_act)
            
            if isinstance(special_node, FinishNode):
                print('\n\n\n Chapter ended with #finish')
                
                current_act_index += 1
                try:
                    current_act = acts[current_act_index]
                    node_index = 0
                    continue
                except IndexError as e:
                    node_index = len(current_act.nodes)
                    continue

            if isinstance(special_node, BookmarkNode):
                target_act = self.acts.get(special_node.act_path)

                if target_act is None:
                    raise ValueError(f'Invalid target act path: {special_node.act_path}')
                
                current_act = target_act
                current_act_index  = acts.index(target_act)
                node_index = self.get_bookmark_index(current_act, special_node)
                
                print(f"Changed the index correctly after")
                
            else:
                node_index += 1
                continue
    
    def render_node(self, node:Node, act:Act) -> BookmarkNode | FinishNode | None:
        if isinstance(node, FinishNode):
            return node
        
        elif isinstance(node, GotoNode):
            bkmk =  get_bookmark_for_goto(node, act, self.acts)
            if bkmk:
                print(f"Trying to #goto bookmark '{bkmk.name}' in act {bkmk.act_path} from act '{act.name}'")
                return bkmk
        
        elif isinstance(node, TextNode):
            text = get_interpolated_text_line(node.text, self.variables)
            print(f"text: {text}")
        
        elif isinstance(node, ChoiceNode):
            print()
            print(f'Choice:')
            for i, option in enumerate(node.options, start=1):
                print(f"[{i}] - {option.text}")
            choice = int(input("> ")) - 1
            selected = node.options[choice]
            
            return self.render_children(selected.children, act)
        
        elif isinstance(node, ConditionNode):
            for branch in node.branches:
                if validate(branch, self.variables):
                    return self.render_children(branch.children, act)
        
        elif isinstance(node, OptionNode):
            return self.render_children(node.children, act)
                
        elif isinstance(node, SetNode):
            if node.variable not in self.variables.keys():
                raise ValueError(f"Invalid variable to set value")
            self.variables[node.variable] = eval(node.expression, self.variables)

    def render_children(self, children:list[Node], act:Act) -> BookmarkNode | FinishNode | None:
        
        for child in children:
            special_node = self.render_node(child, act)
            
            if isinstance(special_node, (BookmarkNode, FinishNode)):
                return special_node
        return None

    def get_bookmark_index(self, act: Act, bookmark: BookmarkNode) -> int:

        for node in act.bookmarks:
            if (
                isinstance(node, BookmarkNode)
                and node.name == bookmark.name
            ):
                return node.position - 1

        raise ValueError(
            f"Bookmark '{bookmark.name}' "
            f"was not found in act '{act.name}'."
        )