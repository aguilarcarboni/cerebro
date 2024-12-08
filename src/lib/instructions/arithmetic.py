from src.lib.instructions.instruction import Instruction

class arithmetic_instruction(Instruction):
    def __init__(self, destination, operation, operand1, operand2):
        super().__init__(destination, operation)
        self.operand1 = operand1
        self.operand2 = operand2
    
    # Update the registers based on the renaming rules 
    def update_registers(self, renaming_rules):
        if self.operand1 in renaming_rules:
            self.operand1 = renaming_rules[self.operand1]
        if self.operand2 in renaming_rules:
            self.operand2 = renaming_rules[self.operand2]
            
    def log_status(self):
        status = (f"instruction '{self.destination} = {self.operand1} {self.operation} {self.operand2}' -issued {self.issue_cycle} -retired {self.retired_cycle}")
        return status