from src.lib.instructions.instruction import Instruction

class load_store_instruction(Instruction):
    
    def __init__(self, destination, operation):
        super().__init__(destination, operation)

    # Method used in register renaming 
    def update_registers(self, renaming_rules):
        if self.operation == "STORE" and self.destination in renaming_rules:
            self.destination = renaming_rules[self.destination]
    
    # Overwritten method 
    def log_status(self):
        if self.operation == "LOAD":
            status = (f'instruction "{self.destination} = {self.operation}" -issued {self.issue_cycle} -retired {self.retired_cycle}')
        else:
            status = (f'instruction "{self.destination} = {self.operation}" -issued {self.issue_cycle} -retired {self.retired_cycle}')
        return status 