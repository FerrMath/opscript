from typing import Any
from pathlib import Path
from app.game.interpreter import Interpreter
from app.game.interpreter.act import Act
from app.game.interpreter.models import BookmarkNode, ChoiceNode, GotoNode, Node, OptionNode, TextNode, ConditionNode, SetNode
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
        
        # prepare the acts data
        self.acts = {
            self.__acts_folder/f"{act}.txt"
            :self.__interpreter.parse_act(act, self.__acts_folder/f"{act}.txt", self.variables)
            for act in data.acts
        }

    
    def run(self):
        for act_value in self.acts.values():
            self.render_act(act_value)
            
    
    def render_act(self, act: Act, start_node_position:int=0) -> Act | None:
    
        node_index = start_node_position
        while node_index < len(act.nodes):
            base_node = act.nodes[node_index]
            
            node = self.render_node(base_node, act)
            if isinstance(node, BookmarkNode):
                print("Got inside the if")
                goto_act = self.acts.get(node.act_path)
                if not goto_act: raise ValueError(f"Invalid act: {goto_act}")
                if goto_act == act:
                    print("Going to bookmark in this act")
                    node_index = node.position+1
                    continue
                else:
                    print(f"Not this act, it's act: {goto_act.name}")
                    return self.render_act(goto_act, node.position+1)
            else:
                node_index += 1
        ...
    
    def render_node(self, node:Node, act:Act) -> Node | None:
        if isinstance(node, GotoNode):
            bkmk =  get_bookmark_for_goto(node, act, self.acts)
            if bkmk:
                print(f"Trying to #goto bookmark '{bkmk.name}' in act {bkmk.act_path} from act '{act.name}'")
                return bkmk
        
        if isinstance(node, TextNode):
            print(f"text: {get_interpolated_text_line(node.text, self.variables)}")
        
        if isinstance(node, ChoiceNode):
            print()
            
            for i, option in enumerate(node.options, start=1):
                print(f"[{i}] - {option.text}")
            
            choice = int(input("> ")) - 1
            selected = node.options[choice]
            
            for child in selected.children:
                self.render_node(child, act)
        
        if isinstance(node, ConditionNode):
            first_true_branch_found = False
            for n in node.branches:
                if first_true_branch_found: break
                if validate(n, self.variables):
                    first_true_branch_found = True
                    for child in n.children:
                        self.render_node(child,act)
        
        if isinstance(node, OptionNode):
            for c in node.children:
                self.render_node(c, act)
                
        if isinstance(node, SetNode):
            if node.variable not in self.variables.keys():
                raise ValueError(f"Invalid variable to set value")
            self.variables[node.variable] = eval(node.expression, self.variables)
