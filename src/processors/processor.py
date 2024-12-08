from src.lib.instructions.instruction import Instruction
from src.lib.instructions.arithmetic import arithmetic_instruction
from src.utils.logger import logger
import time

class processor:

    def __init__(self, functional_units=1):

        # Initialize variables 
        # Instructions: List of instructions to be processed
        # Queue: List of instructions that are currently being processed
        # Cache: List of instructions that have been processed
        
        self.instructions = []         
        self.queue = []
        self.cache = []

        self.functional_units = functional_units
        self.current_cycle = 0
    
    # Simulate a multi-issue processor cycle by cycle
    def simulate(self):
        while self.instructions or self.queue:
            self.current_cycle += 1
            self.schedule()
            self.retire_instructions()
    
    def schedule(self):
        logger.error("critical_failure: Each scheduler schedules instructions differently, implement in subclass.")
        raise Exception("Each scheduler schedules instructions differently, implement in subclass.")
    
    def retire_instructions(self):
        logger.error("critical_failure: Each scheduler retires instructions differently, implement in subclass.")
        raise Exception("Each scheduler retires instructions differently, implement in subclass.")
    
    def schedule_instruction(self, instruction : Instruction):
        # Set issue cycle, expected retriement cycle, and started flag 
        instruction.issue_cycle = self.current_cycle
        instruction.expected = self.current_cycle + instruction.latency()
        instruction.started = True

        # Log status 
        if isinstance(instruction, arithmetic_instruction):
            logger.info(f"[CEREBRO] run schedule_instruction '{instruction.destination} = {instruction.operand1} {instruction.operation} {instruction.operand2}' -cycle {instruction.issue_cycle} -expected {instruction.expected}")
        else:
            logger.info(f"[CEREBRO] run schedule_instruction '{instruction.destination} = {instruction.operation}' -cycle {instruction.issue_cycle} -expected {instruction.expected}")
        time.sleep(0.1)

        # Add instruction to queue for running later
        self.queue.append(instruction)
