import os
import time 
from src.utils.parser import parser
from src.utils.logger import logger

# Instructions
from src.lib.instructions.arithmetic import arithmetic_instruction

# Schedulers
from src.processors.single_instruction import single_instruction_processor
from src.processors.superscalar_in_order import superscalar_in_order
from src.processors.superscalar_out_order import superscalar_out_order
from src.processors.single_instruction_renaming import single_instruction_renaming
from src.processors.superscalar_in_order_rename import superscalar_in_order_rename
from src.processors.superscalar_out_order_rename import superscalar_out_order_rename


"""
from scalar_in_order import SuperscalarInOrder
from scalar_out_order import SuperscalarOutOrder
from rename_single import SingleInOrder_Renaming
from rename_scalar_in_order import SuperscalarInOrder_Renaming
from rename_scalar_out_order import SuperscalarOutOrder_Renaming
"""

def run_cerebro():

    sleep_time = 1
    filename = 'my_example.asm'

    logger.announcement("\n" + "="*80 + "\n" +
                       "█▀▀ █▀▀ █▀█ █▀▀ █▄▄ █▀█ █▀█\n" +
                       "█▄▄ ██▄ █▀▄ ██▄ █▄█ █▀▄ █▄█\n" +
                       "="*80 + "\n" +
                       "SUPERSCALAR_PROCESSOR_INSTRUCTION_SCHEDULER_SIMULATOR v1.0\n" +
                       "="*80 + "\n" +
                       "[CEREBRO] press [ENTER] to_initialize_simulation || type_exit_to_quit...", "matrix")
    
    user_continue = input()
    if user_continue == 'exit':
        logger.announcement("simulation_terminated_by_user", "matrix")
        exit(10)

    """"""
    
    logger.announcement(f"\n" + "="*80 + "\n" + f"[CEREBRO] compile instruction_set_from_program -p {filename}", "matrix")
    time.sleep(sleep_time)

    # Get the file path
    file_path = os.path.join('programs', filename)

    logger.announcement("[CEREBRO] completed" + "\n" + "="*80 + "\n", "matrix")
    time.sleep(sleep_time)

    """
    Simulate the CPUs running the program
    """
    logger.announcement("\n" + "="*80 + "\n" + "[CEREBRO] initialize hardware_processors" + "\n" + "="*80 + "\n", "matrix")
    logger.announcement("loading test_enviornment -part 1", 'matrix')
    time.sleep(sleep_time)

    logger.announcement("\n" + "="*80 + "\n" + "[CEREBRO] single_instruction_processor" + "\n" + "="*80 + "\n", "matrix")
    time.sleep(sleep_time)

    # Single instruction processor
    instructions = parser(file_path)
    single_instruction_1 = single_instruction_processor(functional_units=1)
    single_instruction_1.instructions = instructions
    single_instruction_1.simulate()
    logger.announcement("\n", "matrix")
    time.sleep(sleep_time)

    instructions = parser(file_path)
    single_instruction_2 = single_instruction_processor(functional_units=2)
    single_instruction_2.instructions = instructions
    single_instruction_2.simulate()
    logger.announcement("\n", "matrix")
    time.sleep(sleep_time)

    instructions = parser(file_path)
    single_instruction_3 = single_instruction_processor(functional_units=3)
    single_instruction_3.instructions = instructions
    single_instruction_3.simulate()
    logger.announcement("\n", "matrix")
    time.sleep(sleep_time)

    logger.announcement("\n" + "="*80 + "\n" + "[CEREBRO] scalar_in_order_processor" + "\n" + "="*80 + "\n", "matrix")
    time.sleep(sleep_time)

    # Superscalar in-order processor
    instructions = parser(file_path)
    in_order_scalar_1 = superscalar_in_order(functional_units=1, issues_per_cycle=2)
    in_order_scalar_1.instructions = instructions
    in_order_scalar_1.simulate()
    logger.announcement("\n", "matrix")
    time.sleep(sleep_time)

    instructions = parser(file_path)
    in_order_scalar_2 = superscalar_in_order(functional_units=2, issues_per_cycle=2)
    in_order_scalar_2.instructions = instructions
    in_order_scalar_2.simulate()
    logger.announcement("\n", "matrix")
    time.sleep(sleep_time)

    instructions = parser(file_path)
    in_order_scalar_3 = superscalar_in_order(functional_units=3, issues_per_cycle=2)
    in_order_scalar_3.instructions = instructions
    in_order_scalar_3.simulate()
    logger.announcement("\n", "matrix")
    time.sleep(sleep_time)

    logger.announcement("\n" + "="*80 + "\n" + "[CEREBRO] scalar_out_order_processor" + "\n" + "="*80 + "\n", "matrix")
    time.sleep(sleep_time)

    instructions = parser(file_path)
    out_order_scalar_1 = superscalar_out_order(functional_units=1, issues_per_cycle=2)
    out_order_scalar_1.instructions = instructions
    out_order_scalar_1.simulate()
    logger.announcement("\n", "matrix")
    time.sleep(sleep_time)

    instructions = parser(file_path)
    out_order_scalar_2 = superscalar_out_order(functional_units=2, issues_per_cycle=2)
    out_order_scalar_2.instructions = instructions
    out_order_scalar_2.simulate()
    logger.announcement("\n", "matrix")
    time.sleep(sleep_time)

    instructions = parser(file_path)
    out_order_scalar_3 = superscalar_out_order(functional_units=3, issues_per_cycle=2)
    out_order_scalar_3.instructions = instructions
    out_order_scalar_3.simulate()
    logger.announcement("\n", "matrix")
    time.sleep(sleep_time)

    logger.announcement("loading test_enviornment -part 2", 'matrix')

    logger.announcement("\n" + "="*80 + "\n" + "[CEREBRO] single_instruction_processor_with_renaming" + "\n" + "="*80 + "\n", "matrix")
    time.sleep(sleep_time)

    instructions = parser(file_path)
    single_renaming_1 = single_instruction_renaming(functional_units=1)
    single_renaming_1.instructions = instructions
    single_renaming_1.simulate()
    logger.announcement("\n", "matrix")
    time.sleep(sleep_time)

    instructions = parser(file_path)
    single_renaming_2 = single_instruction_renaming(functional_units=2)
    single_renaming_2.instructions = instructions
    single_renaming_2.simulate()
    logger.announcement("\n", "matrix")
    time.sleep(sleep_time)

    instructions = parser(file_path)
    single_renaming_3 = single_instruction_renaming(functional_units=3)
    single_renaming_3.instructions = instructions
    single_renaming_3.simulate()
    logger.announcement("\n", "matrix")
    time.sleep(sleep_time)

    logger.announcement("\n" + "="*80 + "\n" + "[CEREBRO] scalar_in_order_processor_with_renaming" + "\n" + "="*80 + "\n", "matrix")
    time.sleep(sleep_time)

    instructions = parser(file_path)
    in_order_superscalar_rename_1 = superscalar_in_order_rename(functional_units=1, issues_per_cycle=2)
    in_order_superscalar_rename_1.instructions = instructions
    in_order_superscalar_rename_1.simulate()
    logger.announcement("\n", "matrix")
    time.sleep(sleep_time)

    instructions = parser(file_path)
    in_order_superscalar_rename_2 = superscalar_in_order_rename(functional_units=2, issues_per_cycle=2)
    in_order_superscalar_rename_2.instructions = instructions
    in_order_superscalar_rename_2.simulate()
    logger.announcement("\n", "matrix")
    time.sleep(sleep_time)

    instructions = parser(file_path)
    in_order_superscalar_rename_3 = superscalar_in_order_rename(functional_units=3, issues_per_cycle=2)
    in_order_superscalar_rename_3.instructions = instructions
    in_order_superscalar_rename_3.simulate()
    logger.announcement("\n", "matrix")
    time.sleep(sleep_time)

    logger.announcement("\n" + "="*80 + "\n" + "[CEREBRO] scalar_out_order_processor_with_renaming" + "\n" + "="*80 + "\n", "matrix")
    time.sleep(sleep_time)

    instructions = parser(file_path)
    out_order_superscalar_rename_1 = superscalar_out_order_rename(functional_units=1, issues_per_cycle=2)
    out_order_superscalar_rename_1.instructions = instructions
    out_order_superscalar_rename_1.simulate()
    logger.announcement("\n", "matrix")
    time.sleep(sleep_time)

    instructions = parser(file_path)
    out_order_superscalar_rename_2 = superscalar_out_order_rename(functional_units=2, issues_per_cycle=2)
    out_order_superscalar_rename_2.instructions = instructions
    out_order_superscalar_rename_2.simulate()
    logger.announcement("\n", "matrix")
    time.sleep(sleep_time)

    instructions = parser(file_path)
    out_order_superscalar_rename_3 = superscalar_out_order_rename(functional_units=3, issues_per_cycle=2)
    out_order_superscalar_rename_3.instructions = instructions
    out_order_superscalar_rename_3.simulate()
    logger.announcement("\n", "matrix")
    time.sleep(sleep_time)

    logger.announcement("\n" + "="*80 + "\n" + "[CEREBRO] completed" + "\n" + "="*80 + "\n", "matrix")
    time.sleep(sleep_time)

    """
    Vizualize the results
    """

    # Single instruction processor
    logger.announcement("\n" + "="*80 + "\n" + "[CEREBRO] initialize vizualize_results single_instruction_in_order_processor" + "\n" + "="*80 + "\n", "matrix")
    time.sleep(sleep_time)

    for instruction in single_instruction_1.cache:
        if isinstance(instruction, arithmetic_instruction):
            logger.announcement(f"[CEREBRO] instruction '{instruction.destination} = {instruction.operand1} {instruction.operation} {instruction.operand2}' -issued {instruction.issue_cycle} -retired {instruction.retired_cycle} -expected {instruction.expected}", "info")
        else:
            logger.announcement(f"[CEREBRO] instruction '{instruction.destination} = {instruction.operation}' -issued {instruction.issue_cycle} -retired {instruction.retired_cycle} -expected {instruction.expected}", "info")
    logger.announcement("\n", "matrix")
    time.sleep(sleep_time)

    for instruction in single_instruction_2.cache:
        if isinstance(instruction, arithmetic_instruction):
            logger.announcement(f"[CEREBRO] instruction '{instruction.destination} = {instruction.operand1} {instruction.operation} {instruction.operand2}' -issued {instruction.issue_cycle} -retired {instruction.retired_cycle} -expected {instruction.expected}", "info")
        else:
            logger.announcement(f"[CEREBRO] instruction '{instruction.destination} = {instruction.operation}' -issued {instruction.issue_cycle} -retired {instruction.retired_cycle} -expected {instruction.expected}", "info")
    logger.announcement("\n", "matrix")
    time.sleep(sleep_time)

    for instruction in single_instruction_3.cache:
        if isinstance(instruction, arithmetic_instruction):
            logger.announcement(f"[CEREBRO] instruction '{instruction.destination} = {instruction.operand1} {instruction.operation} {instruction.operand2}' -issued {instruction.issue_cycle} -retired {instruction.retired_cycle} -expected {instruction.expected}", "info")
        else:
            logger.announcement(f"[CEREBRO] instruction '{instruction.destination} = {instruction.operation}' -issued {instruction.issue_cycle} -retired {instruction.retired_cycle} -expected {instruction.expected}", "info")

    logger.announcement("\n" + "="*80 + "\n" + "[CEREBRO] completed" + "\n" + "="*80 + "\n", "matrix")
    time.sleep(sleep_time)

    # Superscalar in-order processor
    logger.announcement("\n" + "="*80 + "\n" + "[CEREBRO] initialize superscalar_in_order_processor" + "\n" + "="*80 + "\n", "matrix")
    time.sleep(sleep_time)

    for instruction in in_order_scalar_1.cache:
        if isinstance(instruction, arithmetic_instruction):
            logger.announcement(f"[CEREBRO] instruction '{instruction.destination} = {instruction.operand1} {instruction.operation} {instruction.operand2}' -issued {instruction.issue_cycle} -retired {instruction.retired_cycle} -expected {instruction.expected}", "info")
        else:
            logger.announcement(f"[CEREBRO] instruction '{instruction.destination} = {instruction.operation}' -issued {instruction.issue_cycle} -retired {instruction.retired_cycle} -expected {instruction.expected}", "info")

    logger.announcement("\n", "matrix")
    time.sleep(sleep_time)

    for instruction in in_order_scalar_2.cache:
        if isinstance(instruction, arithmetic_instruction):
            logger.announcement(f"[CEREBRO] instruction '{instruction.destination} = {instruction.operand1} {instruction.operation} {instruction.operand2}' -issued {instruction.issue_cycle} -retired {instruction.retired_cycle} -expected {instruction.expected}", "info")
        else:
            logger.announcement(f"[CEREBRO] instruction '{instruction.destination} = {instruction.operation}' -issued {instruction.issue_cycle} -retired {instruction.retired_cycle} -expected {instruction.expected}", "info")

    logger.announcement("\n", "matrix")
    time.sleep(sleep_time)

    for instruction in in_order_scalar_3.cache:
        if isinstance(instruction, arithmetic_instruction):
            logger.announcement(f"[CEREBRO] instruction '{instruction.destination} = {instruction.operand1} {instruction.operation} {instruction.operand2}' -issued {instruction.issue_cycle} -retired {instruction.retired_cycle} -expected {instruction.expected}", "info")
        else:
            logger.announcement(f"[CEREBRO] instruction '{instruction.destination} = {instruction.operation}' -issued {instruction.issue_cycle} -retired {instruction.retired_cycle} -expected {instruction.expected}", "info")

    logger.announcement("\n" + "="*80 + "\n" + "[CEREBRO] completed" + "\n" + "="*80 + "\n", "matrix")
    time.sleep(sleep_time)

    # Superscalar out-order processor
    logger.announcement("\n" + "="*80 + "\n" + "[CEREBRO] initialize superscalar_out_order_processor" + "\n" + "="*80 + "\n", "matrix")
    time.sleep(sleep_time)
    for instruction in out_order_scalar_1.cache:
        if isinstance(instruction, arithmetic_instruction):
            logger.announcement(f"[CEREBRO] instruction '{instruction.destination} = {instruction.operand1} {instruction.operation} {instruction.operand2}' -issued {instruction.issue_cycle} -retired {instruction.retired_cycle} -expected {instruction.expected}", "info")
        else:
            logger.announcement(f"[CEREBRO] instruction '{instruction.destination} = {instruction.operation}' -issued {instruction.issue_cycle} -retired {instruction.retired_cycle} -expected {instruction.expected}", "info")

    logger.announcement("\n", "matrix")
    time.sleep(sleep_time)

    for instruction in out_order_scalar_2.cache:
        if isinstance(instruction, arithmetic_instruction):
            logger.announcement(f"[CEREBRO] instruction '{instruction.destination} = {instruction.operand1} {instruction.operation} {instruction.operand2}' -issued {instruction.issue_cycle} -retired {instruction.retired_cycle} -expected {instruction.expected}", "info")
        else:
            logger.announcement(f"[CEREBRO] instruction '{instruction.destination} = {instruction.operation}' -issued {instruction.issue_cycle} -retired {instruction.retired_cycle} -expected {instruction.expected}", "info")

    logger.announcement("\n", "matrix")
    time.sleep(sleep_time)

    for instruction in out_order_scalar_3.cache:
        if isinstance(instruction, arithmetic_instruction):
            logger.announcement(f"[CEREBRO] instruction '{instruction.destination} = {instruction.operand1} {instruction.operation} {instruction.operand2}' -issued {instruction.issue_cycle} -retired {instruction.retired_cycle} -expected {instruction.expected}", "info")
        else:
            logger.announcement(f"[CEREBRO] instruction '{instruction.destination} = {instruction.operation}' -issued {instruction.issue_cycle} -retired {instruction.retired_cycle} -expected {instruction.expected}", "info")

    logger.announcement("\n" + "="*80 + "\n" + "[CEREBRO] completed" + "\n" + "="*80 + "\n", "matrix")
    time.sleep(sleep_time)

    """
    PART 2
    """

    logger.announcement("\n" + "="*80 + "\n" + "[CEREBRO] single_instruction_processor_with_renaming" + "\n" + "="*80 + "\n", "matrix")
    time.sleep(sleep_time)
    for instruction in single_renaming_1.cache:
        if isinstance(instruction, arithmetic_instruction):
            logger.announcement(f"[CEREBRO] instruction '{instruction.destination} = {instruction.operand1} {instruction.operation} {instruction.operand2}' -issued {instruction.issue_cycle} -retired {instruction.retired_cycle} -expected {instruction.expected}", "info")
        else:
            logger.announcement(f"[CEREBRO] instruction '{instruction.destination} = {instruction.operation}' -issued {instruction.issue_cycle} -retired {instruction.retired_cycle} -expected {instruction.expected}", "info")

    logger.announcement("\n", "matrix")
    time.sleep(sleep_time)
    
    for instruction in single_renaming_2.cache:
        if isinstance(instruction, arithmetic_instruction):
            logger.announcement(f"[CEREBRO] instruction '{instruction.destination} = {instruction.operand1} {instruction.operation} {instruction.operand2}' -issued {instruction.issue_cycle} -retired {instruction.retired_cycle} -expected {instruction.expected}", "info")
        else:
            logger.announcement(f"[CEREBRO] instruction '{instruction.destination} = {instruction.operation}' -issued {instruction.issue_cycle} -retired {instruction.retired_cycle} -expected {instruction.expected}", "info")

    logger.announcement("\n", "matrix")
    time.sleep(sleep_time)

    for instruction in single_renaming_3.cache:
        if isinstance(instruction, arithmetic_instruction):
            logger.announcement(f"[CEREBRO] instruction '{instruction.destination} = {instruction.operand1} {instruction.operation} {instruction.operand2}' -issued {instruction.issue_cycle} -retired {instruction.retired_cycle} -expected {instruction.expected}", "info")
        else:
            logger.announcement(f"[CEREBRO] instruction '{instruction.destination} = {instruction.operation}' -issued {instruction.issue_cycle} -retired {instruction.retired_cycle} -expected {instruction.expected}", "info")

    logger.announcement("\n" + "="*80 + "\n" + "[CEREBRO] scalar_in_order_processor_with_renaming" + "\n" + "="*80 + "\n", "matrix")
    time.sleep(sleep_time)

    for instruction in in_order_superscalar_rename_1.cache:
        if isinstance(instruction, arithmetic_instruction):
            logger.announcement(f"[CEREBRO] instruction '{instruction.destination} = {instruction.operand1} {instruction.operation} {instruction.operand2}' -issued {instruction.issue_cycle} -retired {instruction.retired_cycle} -expected {instruction.expected}", "info")
        else:
            logger.announcement(f"[CEREBRO] instruction '{instruction.destination} = {instruction.operation}' -issued {instruction.issue_cycle} -retired {instruction.retired_cycle} -expected {instruction.expected}", "info")

    logger.announcement("\n", "matrix")
    time.sleep(sleep_time)

    for instruction in in_order_superscalar_rename_2.cache:
        if isinstance(instruction, arithmetic_instruction):
            logger.announcement(f"[CEREBRO] instruction '{instruction.destination} = {instruction.operand1} {instruction.operation} {instruction.operand2}' -issued {instruction.issue_cycle} -retired {instruction.retired_cycle} -expected {instruction.expected}", "info")
        else:
            logger.announcement(f"[CEREBRO] instruction '{instruction.destination} = {instruction.operation}' -issued {instruction.issue_cycle} -retired {instruction.retired_cycle} -expected {instruction.expected}", "info")

    logger.announcement("\n", "matrix")
    time.sleep(sleep_time)

    for instruction in in_order_superscalar_rename_3.cache:
        if isinstance(instruction, arithmetic_instruction):
            logger.announcement(f"[CEREBRO] instruction '{instruction.destination} = {instruction.operand1} {instruction.operation} {instruction.operand2}' -issued {instruction.issue_cycle} -retired {instruction.retired_cycle} -expected {instruction.expected}", "info")
        else:
            logger.announcement(f"[CEREBRO] instruction '{instruction.destination} = {instruction.operation}' -issued {instruction.issue_cycle} -retired {instruction.retired_cycle} -expected {instruction.expected}", "info")

    logger.announcement("\n" + "="*80 + "\n" + "[CEREBRO] scalar_out_order_processor_with_renaming" + "\n" + "="*80 + "\n", "matrix")
    time.sleep(sleep_time)
    for instruction in out_order_superscalar_rename_1.cache:
        if isinstance(instruction, arithmetic_instruction):
            logger.announcement(f"[CEREBRO] instruction '{instruction.destination} = {instruction.operand1} {instruction.operation} {instruction.operand2}' -issued {instruction.issue_cycle} -retired {instruction.retired_cycle} -expected {instruction.expected}", "info")
        else:
            logger.announcement(f"[CEREBRO] instruction '{instruction.destination} = {instruction.operation}' -issued {instruction.issue_cycle} -retired {instruction.retired_cycle} -expected {instruction.expected}", "info")

    for instruction in out_order_superscalar_rename_2.cache:
        if isinstance(instruction, arithmetic_instruction):
            logger.announcement(f"[CEREBRO] instruction '{instruction.destination} = {instruction.operand1} {instruction.operation} {instruction.operand2}' -issued {instruction.issue_cycle} -retired {instruction.retired_cycle} -expected {instruction.expected}", "info")
        else:
            logger.announcement(f"[CEREBRO] instruction '{instruction.destination} = {instruction.operation}' -issued {instruction.issue_cycle} -retired {instruction.retired_cycle} -expected {instruction.expected}", "info")

    logger.announcement("\n", "matrix")
    time.sleep(sleep_time)

    for instruction in out_order_superscalar_rename_3.cache:
        if isinstance(instruction, arithmetic_instruction):
            logger.announcement(f"[CEREBRO] instruction '{instruction.destination} = {instruction.operand1} {instruction.operation} {instruction.operand2}' -issued {instruction.issue_cycle} -retired {instruction.retired_cycle} -expected {instruction.expected}", "info")
        else:
            logger.announcement(f"[CEREBRO] instruction '{instruction.destination} = {instruction.operation}' -issued {instruction.issue_cycle} -retired {instruction.retired_cycle} -expected {instruction.expected}", "info")
    
        
    logger.announcement("\n" + "="*80 + "\n" + "[CEREBRO] completed" + "\n" + "="*80 + "\n", "matrix")
    time.sleep(sleep_time)

    logger.announcement("\n" + "="*80 + "\n" + "[CEREBRO] simulation_terminated" + "\n" + "="*80 + "\n", "matrix")
    time.sleep(sleep_time)
    exit(0)

if __name__ == "__main__":
    run_cerebro()