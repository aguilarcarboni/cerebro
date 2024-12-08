from src.processors.processor import processor
from src.lib.instructions.instruction import Instruction
from src.lib.instructions.load_store import load_store_instruction
from src.lib.instructions.arithmetic import arithmetic_instruction
from src.lib.rules import RenamingRules
from src.lib.types.dependencies import DependencyType
from src.utils.logger import logger

class superscalar_in_order_rename(processor):
    """
    A superscalar in-order processor with register renaming capabilities.
    Supports multiple instruction issues per cycle and handles data dependencies.
    """
    def __init__(self, functional_units=4, issues_per_cycle=2):
        super().__init__(functional_units)
        self.issues_per_cycle = issues_per_cycle
        self.renaming_rules = RenamingRules()
    
    def schedule(self):
        """
        Attempts to schedule instructions for execution, respecting the issues_per_cycle limit
        and functional unit availability.
        """
        attempted_issues = 0
        
        for instruction in list(self.instructions):
            if len(self.queue) < self.functional_units and attempted_issues < self.issues_per_cycle:
                attempted_issues += 1
                
                if self.is_ready(instruction):
                    self.schedule_instruction(instruction)
                    self.instructions.remove(instruction)
                else:
                    break

    def retire_instructions(self):
        """
        Retires completed instructions from the execution queue.
        Logs success/failure of retirement attempts.
        """
        for instruction in list(self.queue):
            if self.current_cycle >= instruction.expected:
                # Retire the instruction
                instruction.retire(self.current_cycle)
                self.cache.append(instruction)
                
                # Log successful retirement
                if isinstance(instruction, arithmetic_instruction):
                    logger.success(f"[CEREBRO] run retire_instruction '{instruction.destination} = {instruction.operand1} {instruction.operation} {instruction.operand2}' -issued {instruction.issue_cycle} -cycle {instruction.retired_cycle}")
                else:
                    logger.success(f"[CEREBRO] run retire_instruction '{instruction.destination} = {instruction.operation}' -issued {instruction.issue_cycle} -cycle {instruction.retired_cycle}")
                
                self.queue.remove(instruction)
            else:
                # Log failed retirement attempt
                if isinstance(instruction, arithmetic_instruction):
                    logger.warning(f"[CEREBRO] denied retire_instruction '{instruction.destination} = {instruction.operand1} {instruction.operation} {instruction.operand2}' -expected {instruction.expected} -cycle {self.current_cycle}")
                else:
                    logger.warning(f"[CEREBRO] denied retire_instruction '{instruction.destination} = {instruction.operation}' -expected {instruction.expected} -cycle {self.current_cycle}")
                break

    def is_ready(self, instr: Instruction):
        """
        Checks if an instruction is ready for execution by updating its registers
        and checking for dependencies.
        """
        # Update registers based on current rename map
        instr.update_registers(self.renaming_rules.rename_map)

        # Remove old renaming rule if this isn't a STORE instruction
        if instr.operation != "STORE" and instr.destination in self.renaming_rules.rename_map:
            self.renaming_rules.remove_rule(instr.destination)
        
        return self.check_dependencies(instr) == DependencyType.NONE
    
    def check_dependencies(self, instruction):
        """
        Checks for RAW, WAR, and WAW dependencies between the given instruction
        and instructions currently in the queue.
        
        Returns:
            DependencyType: The type of dependency found, or NONE if no dependencies exist.
        """
        for queued_instruction in self.queue:
            # Check for Read After Write (RAW) dependencies
            if isinstance(instruction, arithmetic_instruction):
                if queued_instruction.destination in [instruction.operand1, instruction.operand2]:
                    return DependencyType.RAW
        
            if isinstance(instruction, load_store_instruction) and instruction.operation == "STORE":
                if queued_instruction.destination == instruction.destination:
                    return DependencyType.RAW

            # Check for Write After Read (WAR) dependencies
            if isinstance(queued_instruction, arithmetic_instruction):
                if instruction.destination in [queued_instruction.operand1, queued_instruction.operand2] and instruction.operation != "STORE":
                    # Attempt register renaming to resolve WAR dependency
                    if not self.renaming_rules.create_rule(instruction.destination):
                        return DependencyType.WAR
                    else:
                        instruction.destination = self.renaming_rules.rename_map[instruction.destination]
        
            # Check for Write After Write (WAW) dependencies
            if instruction.operation != "STORE" and instruction.destination == queued_instruction.destination:
                # Attempt register renaming to resolve WAW dependency
                if not self.renaming_rules.create_rule(instruction.destination):
                    return DependencyType.WAW
                else:
                    instruction.destination = self.renaming_rules.rename_map[instruction.destination]
    
        return DependencyType.NONE
