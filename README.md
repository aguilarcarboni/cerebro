# Cerebro

## Computer Architecture

### Description
Multi-issue processor instruction scheduler simulator that implements various scheduling algorithms to optimize instruction throughput. The simulator provides:

- Comprehensive processor configurations:
  - Single-issue in-order execution
  - Single-issue out-of-order execution
  - Superscalar in-order (2-3 parallel issue slots)
  - Superscalar out-of-order (2-3 parallel issue slots)
- Advanced register renaming capabilities across all modes
- Support for fundamental instruction types:
  - Arithmetic operations (+, -, *)
  - Memory operations (LOAD, STORE)
- Full assembly instruction parsing and simulation engine

### Key Features
- Sophisticated dependency tracking (RAW, WAR, WAW)
- Comprehensive execution logging and analysis

### Instruction Set Architecture
- Register file: 8 general-purpose registers (R0 through R7)
- Operation latencies:
  - Add/Subtract: 1 cycle
  - Multiply: 2 cycles
  - Memory operations: 3 cycles (LOAD/STORE)
- Assembly syntax examples:
  - Memory operations: `R1 = LOAD`, `R2 = STORE`
  - Arithmetic operations: `R0 = R1 + R7`, `R1 = R2 * R3`

### Running the program
Clone the repository at:

```bash
git clone https://github.com/aguilarcarboni/cerebro.git
```

To make sure to have Python and pip installed, run:
```bash
python/python3 --version
pip/pip3 --version
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Then run the simulator:

```bash
./run.sh
```

For debugging and testing, you can run:

```bash
./test.sh
```

### Results 
Scored a ??? on the project.

### created by [@aguilarcarboni](https://github.com/aguilarcarboni/)