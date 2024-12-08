from src.processors.processor import processor
from src.lib.types.dependencies import DependencyType
from src.lib.instructions.load_store import load_store_instruction
from src.lib.instructions.arithmetic import arithmetic_instruction
from src.utils.logger import logger
import time

class superscalar_out_order(processor):
    def __init__(self, functional_units, issues_per_cycle):
        super().__init__(functional_units)
        self.issues_per_cycle = issues_per_cycle
        self.pending_instructions = []
    
    def schedule(self):
        attempted_issues = 0
        for pending in list(self.pending_instructions):
            if len(self.queue) < self.functional_units:
                if self.is_ready_to_execute_from_pending_instructions(pending):
                    self.schedule_instruction(pending)
                    self.pending_instructions.remove(pending)

        # Try to issue new instructions that haven't been overlooked before
        for instruction in list(self.instructions):
            # Check capacity
            if len(self.queue) < self.functional_units and attempted_issues < self.issues_per_cycle:
                attempted_issues += 1
                # Check if it can be scheduled
                if self.is_ready_to_execute_from_instructions(instruction):
                    # Schedule the instruction and remove it from the list
                    self.schedule_instruction(instruction)
                    self.instructions.remove(instruction)
                else:
                    # Add it to pending instructions to wait for dependencies to resolve
                    self.pending_instructions.append(instruction)
                    self.instructions.remove(instruction)
    
    def retire_instructions(self):
        index = 0 
        # Modify original function to go through all queue
        while index < len(self.queue):
            instruction = self.queue[index]
            if self.current_cycle >= instruction.expected and self.can_retire_instructions(instruction):
                instruction.retire(self.current_cycle)
                self.cache.append(instruction)
                
                if isinstance(instruction, arithmetic_instruction):
                    logger.success(f"[CEREBRO] run retire_instruction '{instruction.destination} = {instruction.operand1} {instruction.operation} {instruction.operand2}' -issued {instruction.issue_cycle} -cycle {instruction.retired_cycle}")
                else:
                    logger.success(f"[CEREBRO] run retire_instruction '{instruction.destination} = {instruction.operation}' -issued {instruction.issue_cycle} -cycle {instruction.retired_cycle}")
                time.sleep(0.1)
                
                self.queue.pop(index)
            else:
                if isinstance(instruction, arithmetic_instruction):
                    logger.warning(f"[CEREBRO] denied retire_instruction '{instruction.destination} = {instruction.operand1} {instruction.operation} {instruction.operand2}' -expected {instruction.expected} -cycle {self.current_cycle}")
                else:
                    logger.warning(f"[CEREBRO] denied retire_instruction '{instruction.destination} = {instruction.operation}' -expected {instruction.expected} -cycle {self.current_cycle}")
                index += 1

    # Check data dependencies between instruction and list of instructions
    def check_dependencies(self, instruction, list_of_instructions):
        for queued_instruction in list_of_instructions:

            # Write after read dependency checking
            if isinstance(queued_instruction, arithmetic_instruction) and instruction.destination in [queued_instruction.operand1, queued_instruction.operand2]:
                return DependencyType.WAR
            if isinstance(instruction, load_store_instruction) and instruction.operation == "STORE":
                if queued_instruction.destination == instruction.destination:
                    return DependencyType.WAR

            # Read after write dependency checking
            if isinstance(instruction, arithmetic_instruction) and queued_instruction.destination in [instruction.operand1, instruction.operand2]:
                return DependencyType.RAW
            if isinstance(instruction, load_store_instruction) and instruction.operation == "STORE" and queued_instruction.destination == instruction.destination:
                return DependencyType.RAW
            
            # Write after write dependency checking
            if instruction.destination == queued_instruction.destination:
                return DependencyType.WAW

        return DependencyType.NONE

    def can_retire_instructions(self, instruction):
        for instr in self.queue:
            if instr.issue_cycle < instruction.issue_cycle:
                if isinstance(instr, arithmetic_instruction) and instruction.destination in [instr.operand1, instr.operand2]:
                    return False
                if instr.destination == instruction.destination and instruction.operation != 'STORE':
                    return False
            
        return True 

    def is_ready_to_execute_from_instructions(self, instruction):
        # Check if the instruction has any dependencies with in-progress or pending instructions
        if self.check_dependencies(instruction, self.queue) != DependencyType.NONE:
            return False
        
        if self.check_dependencies(instruction, self.pending_instructions) != DependencyType.NONE:
            return False
        
        return True
    
    def is_ready_to_execute_from_pending_instructions(self, instruction):
        """
        To schedule an instruction from the pending instructions list 
            - It shouldn't write to a register before past instructions write to that same register
            - It shouldn't write to a register before past instructions read from that same register
        These two cases would break the logic due to altering the end results of procedures, thus we must revise them
        """
        # Check if the instruction has any dependencies with in-progress instructions
        if self.check_dependencies(instruction, self.queue) != DependencyType.NONE:
            return False
        
        # Different Format since it should only check instructions that came before itself
        for instr in self.pending_instructions:
            if instr == instruction:
                break
            else:
                # Read after write dependency checking
                if isinstance(instruction, arithmetic_instruction):
                    if instr.destination in [instruction.operand1, instruction.operand2]:
                        return False
                if isinstance(instr, load_store_instruction) and instr.operation == "STORE":
                    if instr.destination == instruction.destination:
                        return False
                
                # Write after read dependency checking
                if isinstance(instr, arithmetic_instruction):
                    if instruction.destination in [instr.operand1, instr.operand2]:
                        return False
                if isinstance(instruction, load_store_instruction) and instruction.operation == "STORE":
                    if instr.destination == instruction.destination:
                        return False
                
                # Write after write dependency checking
                if instruction.destination == instr.destination:
                    return False
        
        return True


    # Overwritten method, we must check that pending instructions are also scheduled and completed.
    def simulate(self):
        while self.instructions or self.queue or self.pending_instructions:
            self.current_cycle += 1
            self.schedule()
            self.retire_instructions()