# quantum_circuit.py

import numpy as np # type: ignore
from quantum_gates import get_operator
from gate_operations_optimized import apply_optimized_gate

class QC:
    """
    Represents and simulates a quantum circuit.
    """
    def __init__(self, num_qubits):
        """
        Initializes the circuit with a number of qubits.
        """
        self.num_qubits = num_qubits
        # Initialize the state vector in the |0...0> state
        self.state_vector = np.zeros(2**self.num_qubits, dtype=complex)
        self.state_vector[0] = 1.0

    def apply_gate(self, gate_name, qubits, noise_prob=0.0, optimized=False):
        """
        Applies a quantum gate to the circuit's state vector.
        If `optimized` is True, uses logical operations instead of matrix multiplication.
        """
        print(f"Applying {gate_name}({','.join(map(str, qubits))})")

        if optimized:
            # Use optimized logical operations
            self.state_vector = apply_optimized_gate(self.state_vector, gate_name, qubits, self.num_qubits)
        else:
            operator = get_operator(gate_name, qubits, self.num_qubits)

            if operator is not None:
                # Apply the gate by multiplying the state vector by the operator matrix
                self.state_vector = operator @ self.state_vector

                # Alternative way using np.dot
                # self.state_vector = np.dot(operator, self.state_vector)

                # Normalize the state vector after applying the gate
                self.state_vector /= np.linalg.norm(self.state_vector)
            else:
                print(f"Warning: Gate '{gate_name}' not recognized.")        # Apply noise after the gate (works for both optimized and matrix modes)
        if noise_prob > 0:
            for qubit_idx in qubits:
                if np.random.rand() < noise_prob:
                    print(f"[NOISE APPLIED] : Bit-flip (X) on qubit {qubit_idx}")
                    noise_op = get_operator('X', [qubit_idx], self.num_qubits)
                    self.state_vector = noise_op @ self.state_vector
                    # Normalize after noise application as well
                    self.state_vector /= np.linalg.norm(self.state_vector)

       
    def measure(self, qubits_to_measure):
        """
        Measures the specified qubits, collapses the state, and returns the result.
        """
        probabilities = np.abs(self.state_vector)**2

        # Debugging: Print the sum of probabilities
        print(f"Sum of probabilities before measurement: {np.sum(probabilities)}")

        if not np.isclose(np.sum(probabilities), 1.0):
            raise ValueError("Probabilities do not sum to 1. Check state vector normalization.")

        # Choose one of the 2^n possible outcomes based on their probabilities
        outcome_index = np.random.choice(2**self.num_qubits, p=probabilities)

        # Collapse the state vector to the measured outcome
        self.state_vector = np.zeros(2**self.num_qubits, dtype=complex)
        self.state_vector[outcome_index] = 1.0

        # Convert the outcome's index to a binary string (e.g., 5 -> '101')
        full_outcome_str = format(outcome_index, f'0{self.num_qubits}b')

        # Extract the results only for the qubits that were measured
        measured_result = "".join([full_outcome_str[i] for i in qubits_to_measure])

        # Debugging: Print the state vector and the measured outcome after measurement
        print(f"State vector after measurement: {self.state_vector}")
        print(f"Measured outcome: {measured_result}")

        return measured_result