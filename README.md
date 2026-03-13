# Quantum Circuit Simulator

A Python-based quantum circuit simulator that supports noiseless and noisy execution modes. This simulator can handle basic quantum gates (H, X, Y, Z, I, CNOT) and measurement operations on multi-qubit systems.

## Features

- **State Vector Simulation**: Simulates quantum circuits using full state vector representation
- **Supported Gates**:
  - Hadamard (H): Single-qubit gate for superposition
  - Pauli-X (X): Single-qubit NOT gate (bit-flip)
  - Pauli-Y (Y): A single-qubit gate that performs a combined bit-flip and phase-flip
  - Pauli-Z (Z): A single-qubit gate that applies a phase-flip on the ∣1⟩ state
  - Identity (I): A single-qubit gate that leaves the quantum state unchanged
  - CNOT: Two-qubit controlled-NOT gate
  - SWAP: Swap two qubit
- **Measurement**: Collapse state vector and extract measurement results for specified qubits
- **Noise Simulation**: Optional bit-flip error model with configurable error probability
- **Circuit File Parser**: Read quantum circuits from human-readable text files

## Requirements

- Python 3.7+
- NumPy

Install dependencies:
```bash
pip install numpy
```

## Project Structure

```
Project/
├── simulator.py                    # Main entry point and CLI
├── quantum_circuit.py              # QC class (state management & gate application)
├── quantum_gates.py                # Gate matrix definitions and operator construction
├── gate_operations_optimized.py   # Optimized logical gate operations (no matrix multiplication)
├── parse_circuit.py                # Circuit file parser
├── file_parser.py                  # Compatibility shim for imports
├── TestCases/
│   ├── circuit1.in                 # Deutsch-Jozsa algorithm example
│   ├── circuit2.in                 # Scalability test (11 qubits)
│   └── circuit3.in                 # Custom test circuit
└── README.md
```

## Usage

### Command Line Interface

```bash
python simulator.py <filepath> {-noiseless | -noise} [-error <probability>] [-optimize]
```

**Arguments:**
- `filepath`: Path to the circuit definition file (required)
- `-noiseless`: Run simulation without noise (mutually exclusive with `-noise`)
- `-noise`: Run simulation with bit-flip noise model (mutually exclusive with `-noiseless`)
- `-error <probability>`: Bit-flip error probability for noisy mode (default: 0.01)
- `-optimize`: Use optimized logical operations instead of matrix multiplication (optional)

### Examples

**Noiseless simulation:**
```bash
python simulator.py TestCases/circuit1.in -noiseless
```

**Noisy simulation with custom error rate:**
```bash
python simulator.py TestCases/circuit1.in -noise -error 0.05
```

**Optimized mode (faster for large circuits):**
```bash
python simulator.py TestCases/circuit2.in -noiseless -optimize
```

## Circuit File Format

Circuit files use a simple text-based format:

```
// Comments start with //
circuit: <N> qubits

// Gate syntax: GATE_NAME(qubit_indices)
H(0)              // Hadamard on qubit 0
X(2)              // Pauli-X on qubit 2
CNOT(0,1)         // CNOT with control=0, target=1

// Measurement syntax: measure start..end
measure 0..2      // Measure qubits 0, 1, 2
```

### Example Circuit Files

**circuit1.in** - Deutsch-Jozsa Algorithm (3 qubits):
```
// Deutsch–Jozsa for balanced f(x) = x0 XOR x1
circuit: 3 qubits
X(2)
H(0)
H(1)
H(2)
CNOT(0,2)
CNOT(1,2)
H(0)
H(1)
measure 0..1
```

**circuit2.in** - Scalability Test (11 qubits):
```
// Scalability sanity test: many single-qubit ops
circuit: 11 qubits
X(0)
X(1)
H(2)
X(3)
X(4)
X(5)
X(6)
X(7)
X(8)
X(9)
X(10)
measure 0..10
```

## Implementation Details

### State Vector Representation

The simulator uses a full state vector of size $2^n$ for $n$ qubits. The state is initialized to $|0...0\rangle$ and evolved by applying unitary gate operators.

### Gate Application

**Matrix Mode (default):**
Single-qubit gates are expanded to $2^n \times 2^n$ matrices using tensor products:
$$U_{\text{full}} = I \otimes I \otimes ... \otimes G \otimes ... \otimes I$$

CNOT gates are constructed by iterating through basis states and applying the controlled bit-flip logic.

**Optimized Mode (`-optimize` flag):**
Gates are applied using logical operations directly on the state vector without constructing full matrices:
- X gate: Swaps amplitudes between basis states differing in the target qubit
- H gate: Creates superposition by redistributing amplitudes with appropriate phase factors
- Z gate: Applies phase flip by multiplying amplitude by -1 when target qubit is |1⟩
- CNOT: Conditionally swaps amplitudes based on control qubit state

Optimized mode is more memory-efficient and can be faster for certain operations.

### Measurement

Measurement follows the standard quantum mechanics protocol:
1. Compute probabilities: $p_i = |\langle i | \psi \rangle|^2$
2. Sample outcome based on probability distribution
3. Collapse state vector to measured basis state
4. Extract measurement result for specified qubits

### Noise Model

In noisy mode, after each gate application, bit-flip errors (X gates) are applied to each involved qubit with probability $p_{\text{error}}$:
- After gate $G$ on qubits $\{q_1, q_2, ...\}$, apply $X(q_i)$ with probability $p_{\text{error}}$ for each $q_i$

## Module Descriptions

### `simulator.py`
- CLI argument parsing (filepath, noise mode, error probability, optimize flag)
- Main simulation loop
- Instruction execution orchestration

### `quantum_circuit.py`
- `QC` class for quantum circuit simulation
- State vector management and initialization
- Gate application with optional noise and optimization modes
- Measurement and state collapse with probability calculation

### `quantum_gates.py`
- Gate matrix definitions (H, X, Y, Z, I, SWAP)
- `get_operator()`: Factory function to get appropriate gate operator
- `get_single_qubit_operator()`: Constructs full operator for single-qubit gates using tensor products
- `get_cnot_operator()`: Constructs full CNOT operator matrix
- `get_swap_operator()`: Constructs full SWAP operator matrix

### `gate_operations_optimized.py`
- `apply_optimized_gate()`: Dispatcher for optimized gate operations
- Optimized implementations of all gates using logical operations instead of matrix multiplication
- Functions: `apply_optimized_x`, `apply_optimized_h`, `apply_optimized_y`, `apply_optimized_z`, `apply_optimized_i`, `apply_optimized_cnot`, `apply_optimized_swap`
- More memory-efficient for large qubit systems

### `parse_circuit.py`
- `parse_circuit_file()`: Parses circuit definition files
- Supports single qubit measurement (`measure 0`) and range measurement (`measure 0..2`)
- Returns tuple: `(num_qubits, instructions_list)`
- Instruction format: `(operation_name, [qubit_indices])`
- Error handling for malformed instructions

## Sample Output

```
--- Starting Quantum Simulation ---
Mode: Noiseless
Qubits: 3

Applying X(2)
Applying H(0)
Applying H(1)
Applying H(2)
Applying CNOT(0,2)
Applying CNOT(1,2)
Applying H(0)
Applying H(1)

Measuring qubits [0, 1]...

--- Simulation Complete ---
Final Measurement Result for qubits [0, 1]: 11
```

## Limitations

- Supports H, X, Y, Z, I, SWAP, and CNOT gates (extensible design for adding more)
- Noise model is limited to bit-flip errors (no phase-flip or depolarizing noise)
- Memory requirement scales as $O(2^n)$ for $n$ qubits in state vector mode
- No support for density matrix representation
- Single measurement per circuit execution
- Noise simulation only available in matrix mode (not in optimized mode)


## Author

Md. Ahsan Habib \
CS PhD Student \
Tulane University