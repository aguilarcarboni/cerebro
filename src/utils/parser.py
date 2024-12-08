from src.lib.instructions.load_store import load_store_instruction
from src.lib.instructions.arithmetic import arithmetic_instruction  
from src.utils.logger import logger

def parser(filename):
    """
    Reads and parses assembly-like instructions from a file.

    The function processes instructions in the format:
    - LOAD/STORE operations: dest = LOAD/STORE
    - Arithmetic operations: dest = src1 op src2 where op can be +, -, or *

    Args:
        filename (str): Path to the file containing instructions

    Returns:
        list: List of Instruction objects (LoadStoreInstruction or ThreeRegInstruction)

    Raises:
        Exception: If an invalid operation is encountered in the file
        SystemExit: If the file cannot be found or opened
    """
    instructions = []
    try:
        with open(filename, 'r') as f:

            for line in f:
                line = line.strip()
                if line:

                    # Split the line into register destination and the operation to be performed
                    equation = line.replace(" ","").split("=")
                    destination = equation[0]

                    # Split the operation side into operators and operands
                    if 'LOAD' in equation[1]:   
                        instruction = load_store_instruction(destination=destination, operation='LOAD')
                    elif 'STORE' in equation[1]:
                        instruction = load_store_instruction(destination=destination, operation='STORE')
                    elif '+' in equation[1]:
                        operand1, operand2 = equation[1].split('+')
                        instruction = arithmetic_instruction(destination=destination, operation='+', operand1=operand1, operand2=operand2)
                    elif '-' in equation[1]:
                        operand1, operand2 = equation[1].split('-')
                        instruction = arithmetic_instruction(destination=destination, operation='-', operand1=operand1, operand2=operand2)
                    elif '*' in equation[1]:
                        operand1, operand2 = equation[1].split('*')
                        instruction = arithmetic_instruction(destination=destination, operation='*', operand1=operand1, operand2=operand2)
                    else:
                        logger.error(f"invalid_operation_in_line - {line}")
                        raise Exception(f"invalid_operation_in_line - {line}")

                    instructions.append(instruction)

    except:
        logger.error(f'terminating_program: error_parsing_file - {filename}')
        exit(1)
    
    return instructions