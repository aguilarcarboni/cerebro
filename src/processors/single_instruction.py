from src.processors.processor import processor
from src.lib.types.dependencies import DependencyType
from src.lib.instructions.arithmetic import arithmetic_instruction
from src.utils.logger import logger
import time

class single_instruction_processor(processor):
    
    def __init__(self, functional_units=1):
        super().__init__(functional_units)

    # Make sure there are instructions queued up and check for open functional units 
    def schedule(self):
        if len(self.queue) < self.functional_units and self.instructions:
            instruction = self.instructions[0]

            # Check if the instruction has no dependencies
            if self.check_dependencies(instruction) == DependencyType.NONE:
                self.schedule_instruction(instruction)

                # Remove instruction from instructions list so it is not run again 
                self.instructions.remove(instruction)
    
    def retire_instructions(self):
        for instruction in list(self.queue):

            # Retire instruction if the clock cycle is passed the instructions expected retriement cycle 
            if self.current_cycle >= instruction.expected:
                instruction.retire(self.current_cycle)

                # Add instruction to cache for vizualization and log status 
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
 
 
    def check_dependencies(self, instruction):

        # Follow rules seen in class
        for queued_instruction in self.queue:

            if queued_instruction == instruction:
                return DependencyType.NONE
            
            # Write after write dependency checking 
            if instruction.operation != "STORE" and instruction.destination == queued_instruction.destination:
                return DependencyType.WAW
            
            # Write after read dependency checking 
            if isinstance(queued_instruction, arithmetic_instruction): 
                if instruction.destination in [queued_instruction.operand1, queued_instruction.operand2] and instruction.operation != "STORE":
                    return DependencyType.WAR
                
            if queued_instruction.operation == "STORE" and queued_instruction.destination == instruction.destination:
                    return DependencyType.WAR
            
            # Read after write dependency checking            
            if queued_instruction.operation == "STORE" and instruction.operation == "STORE":
                return DependencyType.RAW
            
            if isinstance(instruction, arithmetic_instruction):
                if queued_instruction.destination in [instruction.operand1, instruction.operand2] and queued_instruction.operation !=  "STORE":
                    return DependencyType.RAW
            
            if isinstance(instruction, arithmetic_instruction) and instruction.operation == "STORE":
                if queued_instruction.destination == instruction.destination:
                    return DependencyType.RAW

        return DependencyType.NONE