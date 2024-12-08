from src.processors.processor import processor
from src.lib.types.dependencies import DependencyType
from src.lib.instructions.instruction import Instruction
from src.lib.instructions.load_store import load_store_instruction
from src.lib.instructions.arithmetic import arithmetic_instruction
from src.lib.rules import RenamingRules
from src.utils.logger import logger
import time

class single_instruction_renaming(processor):
    def __init__(self, functional_units=1):
        super().__init__(functional_units)
        self.renaming_rules = RenamingRules()
    
    # Make sure there are instructions queued up and check for open functional units 
    def schedule(self):
        if len(self.queue) < self.functional_units and self.instructions:
            instruction = self.instructions[0]

            # Check if the instruction has no dependencies and is ready to execute
            if self.can_be_executed(instruction):
                self.schedule_instruction(instruction)

                # Remove instruction from instructions list so it is not run again 
                self.instructions.remove(instruction)

    def retire_instructions(self):

        for instruction in list(self.queue):

            # Retire instruction if the clock cycle is passed the instructions expected retriement cycle 
            if self.current_cycle >= instruction.expected:
                instruction.retire(self.current_cycle)

                # Add instruction to cache and log status 
                self.cache.append(instruction)
                if isinstance(instruction, arithmetic_instruction):
                    logger.success(f"[CEREBRO] run retire_instruction '{instruction.destination} = {instruction.operand1} {instruction.operation} {instruction.operand2}' -issued {instruction.issue_cycle} -cycle {instruction.retired_cycle}")
                else:
                    logger.success(f"[CEREBRO] run retire_instruction '{instruction.destination} = {instruction.operation}' -issued {instruction.issue_cycle} -cycle {instruction.retired_cycle}")
                time.sleep(0.1)

                # Remove instruction from queue so it is not run again 
                self.queue.remove(instruction)
            else:
                # Deny instruction if it's still to early to retire instruction 
                if isinstance(instruction, arithmetic_instruction):
                    logger.warning(f"[CEREBRO] denied retire_instruction '{instruction.destination} = {instruction.operand1} {instruction.operation} {instruction.operand2}' -expected {instruction.expected} -cycle {self.current_cycle}")
                else:
                    logger.warning(f"[CEREBRO] denied retire_instruction '{instruction.destination} = {instruction.operation}' -expected {instruction.expected} -cycle {self.current_cycle}")
                break

    def can_be_executed(self, instruction : Instruction):
        instruction.update_registers(self.renaming_rules.rename_map)

        # Remove renaming rule if it's not a store operation and the destination register is in the renaming map
        if instruction.operation != "STORE" and instruction.destination in self.renaming_rules.rename_map:
            self.renaming_rules.remove_rule(instruction.destination)
        
        return self.check_dependencies(instruction) == DependencyType.NONE
    
    def check_dependencies(self, instruction):
        for queued_instruction in self.queue:

            # Read after write dependency when storing
            # No way of resolving
            if isinstance(instruction, load_store_instruction) and instruction.operation == "STORE" and queued_instruction.operation != "STORE":
                if queued_instruction.destination == instruction.destination:
                    return DependencyType.RAW

            # Read after write dependency, no way of resolving
            if isinstance(instruction, arithmetic_instruction):
                if queued_instruction.destination in [instruction.operand1, instruction.operand2]:
                    return DependencyType.RAW
            
            # Write after read dependency
            # Attempt renaming
            if isinstance(queued_instruction, arithmetic_instruction):
                if instruction.destination in [queued_instruction.operand1, queued_instruction.operand2] and instruction.operation != "STORE":
                    if not self.renaming_rules.create_rule(instruction.destination):
                        return DependencyType.WAR
                    else:        
                        # If it can be resolved the destination reg should change
                        instruction.destination = self.renaming_rules.rename_map[instruction.destination]
            if queued_instruction.operation == "STORE" and queued_instruction.destination == instruction.destination and instruction.operation != "STORE":
                if not self.renaming_rules.create_rule(instruction.destination):
                    return DependencyType.WAR
                else:
                    instruction.destination = self.renaming_rules.rename_map[instruction.destination]
            
            # Write after write dependency
            # Attempt renaming
            if instruction.operation != "STORE" and instruction.destination == queued_instruction.destination:
                if not self.renaming_rules.create_rule(instruction.destination):
                    return DependencyType.WAW
                else:
                     # If it can be resolved the destination reg should change
                    instruction.destination = self.renaming_rules.rename_map[instruction.destination]
        
        # No dependencies found
        return DependencyType.NONE
