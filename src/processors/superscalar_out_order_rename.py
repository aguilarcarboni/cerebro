from src.processors.processor import processor
from src.lib.types.dependencies import DependencyType
from src.lib.instructions.load_store import load_store_instruction
from src.lib.instructions.arithmetic import arithmetic_instruction
from src.lib.rules import RenamingRules
from src.utils.logger import logger

class superscalar_out_order_rename(processor):
    def __init__(self, functional_units=4, issues_per_cycle=2):
        super().__init__(functional_units)
        self.issues_per_cycle = issues_per_cycle
        self.pending_instructions = []
        self.renaming_rules = RenamingRules()

    def schedule(self):
        attempted_issues = 0
        for pending in self.pending_instructions[:]:
            if len(self.queue) < self.functional_units:
                if self.is_ready_to_execute_from_pending_instructions(pending):
                    self.schedule_instruction(pending)
                    self.pending_instructions.remove(pending)
        
        for instruction in self.instructions[:]:
            if len(self.queue) < self.functional_units and attempted_issues < self.issues_per_cycle:
                attempted_issues += 1
                if self.is_ready_to_execute_from_instructions(instruction):
                    self.schedule_instruction(instruction)
                    self.instructions.remove(instruction)
                else:
                    self.pending_instructions.append(instruction)
                    self.instructions.remove(instruction)

        
    def retire_instructions(self):
        i = 0 
        while i < len(self.queue):
            instr = self.queue[i]
            if self.current_cycle >= instr.expected and self.can_retire_instructions(instr):
                instr.retire(self.current_cycle)
                self.cache.append(instr)
                if isinstance(instr, arithmetic_instruction):
                    logger.success(f"[CEREBRO] run retire_instruction '{instr.destination} = {instr.operand1} {instr.operation} {instr.operand2}' -issued {instr.issue_cycle} -cycle {instr.retired_cycle}")
                else:
                    logger.success(f"[CEREBRO] run retire_instruction '{instr.destination} = {instr.operation}' -issued {instr.issue_cycle} -cycle {instr.retired_cycle}")
                self.queue.pop(i)
            else:
                i += 1

    def is_ready_to_execute_from_instructions(self, instruction):
        instruction.update_registers(self.renaming_rules.rename_map)

        if instruction.destination in self.renaming_rules.rename_map and instruction.operation != "STORE":
            self.renaming_rules.remove_rule(instruction.destination)

        if self.check_dependencies(instruction, self.pending_instructions) != DependencyType.NONE:
            return False
        
        if self.check_dependencies(instruction, self.queue) != DependencyType.NONE:
            return False 
        else:
            return True 
    
    def check_dependencies(self, instruction, instruction_list):
        for instr in instruction_list:
            if instr == instruction:
                return DependencyType.NONE
            
            if isinstance(instruction, arithmetic_instruction):
                if instr.destination in [instruction.operand1, instruction.operand2]:
                    return DependencyType.RAW
            
            if isinstance(instruction, load_store_instruction) and instruction.operation == "STORE" and instr.operation != "STORE":
                if instr.destination == instruction.destination:
                    return DependencyType.RAW
            
            if isinstance(instr, arithmetic_instruction):
                if instruction.destination in [instr.operand1, instr.operand2] and instruction.operation != "STORE":
                    if not self.renaming_rules.create_rule(instruction.destination):
                        return DependencyType.WAR
                    else:        
                        instruction.destination = self.renaming_rules.rename_map[instruction.destination]
            if instr.operation == "STORE" and instr.destination == instruction.destination and instruction.operation != "STORE":
                if not self.renaming_rules.create_rule(instruction.destination):
                    return DependencyType.WAR
                else:
                    instruction.destination = self.renaming_rules.rename_map[instruction.destination]
            
            if instruction.operation != "STORE" and instruction.destination == instr.destination:
                if not self.renaming_rules.create_rule(instruction.destination):
                    return DependencyType.WAW
                else:
                    instruction.destination = self.renaming_rules.rename_map[instruction.destination]
        return DependencyType.NONE
    
    def is_ready_to_execute_from_pending_instructions(self, instruction):
        if instruction.destination in self.renaming_rules.rename_map and instruction.operation != "STORE":
            self.renaming_rules.remove_rule(instruction.destination)

        if self.check_dependencies(instruction, self.pending_instructions) != DependencyType.NONE:
            return False
        
        if self.check_dependencies(instruction, self.queue) != DependencyType.NONE:
            return False 
        else:
            return True 
        
    def can_retire_instructions(self, instruction):
        for instr in self.queue:
            if instr.issue_cycle < instruction.issue_cycle:
                if isinstance(instr, arithmetic_instruction) and instruction.destination in [instr.operand1, instr.operand2]:
                    return False
                if instr.destination == instruction.destination and instruction.operation != 'STORE':
                    return False
            
        return True 
    
    def run(self):
        while self.instructions or self.queue or self.pending_instructions:
            self.execute_cycle()
    