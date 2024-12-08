# Here I am just creating a simple dictionary to store the usable physical registers

class RenamingRules:

    def __init__(self, max_registers=8):
        self.rename_map = {}
        self.max_registers = max_registers
        self.available_registers = set([f"S{i}" for i in range(0, max_registers)]) 
    
    def create_rule(self, logical_register):
        if logical_register not in self.rename_map:
            if not self.available_registers:
                return False
            
            physical_register = self.available_registers.pop()
            self.rename_map[logical_register] = physical_register
            return True
        return False

    def remove_rule(self, logical_register):
        if logical_register in self.rename_map:
            physical_register = self.rename_map.pop(logical_register)
            self.available_registers.add(physical_register)
            return True
        return False