from typing import Any
from pathlib import Path
from app.game.interpreter import Interpreter
from app.game.interpreter.act import Act
from app.game.interpreter.models import ChoiceNode, Node, OptionNode, TextNode, ConditionNode
from app.game.interpreter.runtime.conditions import validate

class Game:
    def __init__(self, game_folder:Path) -> None:
        self.__acts_folder:Path = game_folder / 'acts'
        self.__interpreter:Interpreter = Interpreter(self.__acts_folder)
        self.meta:dict[str,str] = {}
        self.variables:dict[str,Any] = {}
        self.acts: list[Act] = [] # Temp will create Act class later
    
    def setup(self):
        # Get the meta and variables data
        data = self.__interpreter.parse_setup()
        self.meta = data.meta
        self.variables = data.variables
        
        # prepare the acts data
        act_names = data.acts
        for act in act_names:
            act_path = self.__acts_folder / f'{act}.txt'
            self.acts.append(self.__interpreter.parse_act(act, act_path, self.variables))
    
    def run(self):
        for act in self.acts:
            print(f'\n\n*** Starting act: {act.name} ***')
            for node in act.nodes:
                self.render_node(node)
            print(f'*** Ending act {act.name} ***')
                
    
    def render_node(self, node:Node):
        if isinstance(node, TextNode):
            print(f"text: {node.text}")
        
        if isinstance(node, ChoiceNode):
            print()
            
            for i, option in enumerate(node.options, start=1):
                print(f"[{i}] - {option.text}")
            
            choice = int(input("> ")) - 1
            selected = node.options[choice]
            
            for child in selected.children:
                self.render_node(child)
        
        if isinstance(node, ConditionNode):
            first_true_branch_found = False
            for n in node.branches:
                if validate(n.condition, self.variables) and not first_true_branch_found:
                    first_true_branch_found = True
                    for child in n.children:
                        self.render_node(child)
        
        if isinstance(node, OptionNode):
            print(f'Option: {node.text}')
            print("Printing children of option")
            for c in node.children:
                self.render_node(c)