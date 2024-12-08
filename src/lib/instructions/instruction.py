from src.utils.logger import logger

class Instruction:
    
    def __init__(self, destination, operation):

        self.destination = destination
        self.operation = operation
        
        self.issue_cycle : int = None 
        self.expected : int = None 
        self.started : bool = False 
        self.retired_cycle : int = 0 
    
    def print(self):
        logger.error("must_be_implemented_in_subclass")
        raise Exception("must_be_implemented_in_subclass")

    def log_status(self):
        logger.error("must_be_implemented_in_subclass")
        raise Exception("must_be_implemented_in_subclass")
    
    def update_registers(self, renaming_rules):
        logger.error("must_be_implemented_in_subclass")
        raise Exception("must_be_implemented_in_subclass")
    
    def retire(self, cycle):
        self.retired_cycle = cycle

    def latency(self):
        match self.operation:
            case '+' | '-':
                return 1
            case '*':
                return 2
            case 'LOAD' | 'STORE':
                return 3
            case _:
                raise Exception("error assign_latency_to_instruction: invalid_instruction")