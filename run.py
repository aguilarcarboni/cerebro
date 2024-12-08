import os
from src.utils.parser import parser
from src.processors.single_instruction import single_instruction_processor
from src.processors.superscalar_in_order import superscalar_in_order
from src.processors.superscalar_out_order import superscalar_out_order
from src.processors.single_instruction_renaming import single_instruction_renaming
from src.processors.superscalar_in_order_rename import superscalar_in_order_rename
from src.processors.superscalar_out_order_rename import superscalar_out_order_rename
from src.lib.instructions.arithmetic import arithmetic_instruction
from src.utils.logger import logger

def run_cerebro(filename='class_example.asm', functional_units=3, processor_type='single'):
    """
    Run the CPU simulator with configurable parameters.
    
    Args:
        filename (str): The assembly file to process
        functional_units (int): Number of parallel functional units
        processor_type (str): Type of processor to simulate
            - 'single': Single instruction processor
            - 'in_order': Superscalar in-order processor
            - 'out_order': Superscalar out-of-order processor
            - 'single_rename': Single instruction with register renaming
            - 'in_order_rename': Superscalar in-order with register renaming
            - 'out_order_rename': Superscalar out-of-order with register renaming
    """
    sleep_time = 1
    issues_per_cycle = 2

    logger.announcement("\n" + "="*80 + "\n" +
                       "█▀▀ █▀▀ █▀█ █▀▀ █▄▄ █▀█ █▀█\n" +
                       "█▄▄ ██▄ █▀▄ ██▄ █▄█ █▀▄ █▄█\n" +
                       "="*80 + "\n" +
                       "SUPERSCALAR_PROCESSOR_INSTRUCTION_SCHEDULER_SIMULATOR v1.0\n" +
                       "="*80 + "\n", "matrix")

    # Get the file path and parse instructions
    file_path = os.path.join('programs', filename)
    logger.announcement(f"[CEREBRO] compile instruction_set_from_program -p {filename}", "matrix")
    instructions = parser(file_path)

    logger.announcement(f"\n[CEREBRO] initialize {processor_type}_processor with {functional_units} functional_units\n", "matrix")

    # Initialize the appropriate processor based on type
    processor = None
    if processor_type == 'single':
        processor = single_instruction_processor(functional_units=functional_units)
    elif processor_type == 'in_order':
        processor = superscalar_in_order(functional_units=functional_units, issues_per_cycle=issues_per_cycle)
    elif processor_type == 'out_order':
        processor = superscalar_out_order(functional_units=functional_units, issues_per_cycle=issues_per_cycle)
    elif processor_type == 'single_rename':
        processor = single_instruction_renaming(functional_units=functional_units)
    elif processor_type == 'in_order_rename':
        processor = superscalar_in_order_rename(functional_units=functional_units, issues_per_cycle=issues_per_cycle)
    elif processor_type == 'out_order_rename':
        processor = superscalar_out_order_rename(functional_units=functional_units, issues_per_cycle=issues_per_cycle)
    else:
        logger.announcement(f"[ERROR] invalid_processor_type: {processor_type}", "error")
        exit(1)

    # Set instructions and run simulation
    processor.instructions = instructions
    processor.simulate()

    # Display results
    logger.announcement("\n" + "="*80 + "\n" + f"[CEREBRO] results for {processor_type}_processor\n" + "="*80 + "\n", "matrix")
    
    for instruction in processor.cache:
        if isinstance(instruction, arithmetic_instruction):
            logger.announcement(
                f"[CEREBRO] instruction '{instruction.destination} = {instruction.operand1} {instruction.operation} {instruction.operand2}' "
                f"-issued {instruction.issue_cycle} -retired {instruction.retired_cycle} -expected {instruction.expected}", 
                "info"
            )
        else:
            logger.announcement(
                f"[CEREBRO] instruction '{instruction.destination} = {instruction.operation}' "
                f"-issued {instruction.issue_cycle} -retired {instruction.retired_cycle} -expected {instruction.expected}", 
                "info"
            )
    
    logger.announcement("\n" + "="*80 + "\n" + "[CEREBRO] simulation_terminated" + "\n" + "="*80 + "\n", "matrix")

if __name__ == "__main__":
    logger.announcement("[CEREBRO] enter filename:", "matrix")
    filename = input()
    
    logger.announcement("[CEREBRO] enter number of functional_units:", "matrix")
    functional_units = int(input())
    
    logger.announcement("[CEREBRO] enter processor_type -options: single, in_order, out_order, single_rename, in_order_rename, out_order_rename:", "matrix")
    processor_type = input()

    run_cerebro(
        filename=filename,
        functional_units=functional_units,
        processor_type=processor_type
    )