from src.processors.processor import processor
from src.lib.types.dependencies import DependencyType
from src.lib.instructions.arithmetic import arithmetic_instruction
from src.utils.logger import logger
import time

class superscalar_in_order(processor):

    def __init__(self, functional_units=4, issues_per_cycle=2):
        super().__init__(functional_units)
        self.issues_per_cycle = issues_per_cycle
    
    def schedule(self):
        attempted_issues = 0
        for instruction in list(self.instructions):
            if len(self.queue) < self.functional_units and attempted_issues < self.issues_per_cycle:
                attempted_issues += 1
                if self.check_dependencies(instruction) == DependencyType.NONE:
                    self.schedule_instruction(instruction)
                    self.instructions.remove(instruction)
                else:
                    break
    
    def retire_instructions(self):
        for instruction in list(self.queue):
            if self.current_cycle >= instruction.expected:
                instruction.retire(self.current_cycle)
                
                # Add instruction to cache and log status
                self.cache.append(instruction)
                if isinstance(instruction, arithmetic_instruction):
                    logger.success(f"[CEREBRO] run retire_instruction '{instruction.destination} = {instruction.operand1} {instruction.operation} {instruction.operand2}' -issued {instruction.issue_cycle} -cycle {instruction.retired_cycle}")
                else:
                    logger.success(f"[CEREBRO] run retire_instruction '{instruction.destination} = {instruction.operation}' -issued {instruction.issue_cycle} -cycle {instruction.retired_cycle}")
                time.sleep(0.1)

                self.queue.remove(instruction)
            else:
                # Log denied retirements
                if isinstance(instruction, arithmetic_instruction):
                    logger.warning(f"[CEREBRO] denied retire_instruction '{instruction.destination} = {instruction.operand1} {instruction.operation} {instruction.operand2}' -expected {instruction.expected} -cycle {self.current_cycle}")
                else:
                    logger.warning(f"[CEREBRO] denied retire_instruction '{instruction.destination} = {instruction.operation}' -expected {instruction.expected} -cycle {self.current_cycle}")
                break

    def check_dependencies(self, instruction):
        # Use examples given in class
        for queued_instruction in list(self.queue):
            # Write after read dependency
            if isinstance(queued_instruction, arithmetic_instruction) and instruction.destination in [queued_instruction.operand1, queued_instruction.operand2]:
                return DependencyType.WAW
            
            # Read after write dependency
            if (isinstance(instruction, arithmetic_instruction)) and queued_instruction.destination in [instruction.operand1, instruction.operand2]:
                return DependencyType.RAW
            if instruction.operation == "STORE" and queued_instruction.destination == instruction.destination:
                return DependencyType.RAW
            
            # Write after write dependency
            if instruction.destination == queued_instruction.destination:
                return DependencyType.WAW

        return DependencyType.NONE