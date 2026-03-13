# optimized_gate_operations.py

import numpy as np # type: ignore

def apply_optimized_gate(state_vector, gate_name, qubits, num_qubits):
    """
    Applies a quantum gate logically without constructing the full 2^n x 2^n matrix.

    Parameters:
        state_vector (np.ndarray): The current state vector of the quantum system.
        gate_name (str): The name of the gate ('X', 'H', etc.).
        qubits (list): The indices of the qubits to which the gate is applied.
        num_qubits (int): The total number of qubits in the system.

    Returns:
        np.ndarray: The updated state vector after applying the gate.
    """
    if gate_name == 'X':
        return apply_optimized_x(state_vector, qubits[0], num_qubits)
    elif gate_name == 'H':
        return apply_optimized_h(state_vector, qubits[0], num_qubits)
    elif gate_name == 'Y':
        return apply_optimized_y(state_vector, qubits[0], num_qubits)
    elif gate_name == 'Z':
        return apply_optimized_z(state_vector, qubits[0], num_qubits)
    elif gate_name == 'I':
        return apply_optimized_i(state_vector, qubits[0], num_qubits)
    elif gate_name == 'CNOT':
        return apply_optimized_cnot(state_vector, qubits[0], qubits[1], num_qubits)
    elif gate_name == 'SWAP':
        return apply_optimized_swap(state_vector, qubits[0], qubits[1], num_qubits)
    else:
        raise NotImplementedError(f"Gate {gate_name} is not implemented for optimized operations.")


def apply_optimized_x(state_vector, target_qubit, num_qubits):
    """
    Applies the Pauli-X (bit-flip) gate logically to the target qubit.
    """
    # print(state_vector, target_qubit, num_qubits)
    new_state_vector = np.zeros_like(state_vector)
    for i in range(len(state_vector)):
        basis_state = format(i, f'0{num_qubits}b')
        # print(basis_state)
        flipped_state = list(basis_state)
        flipped_state[target_qubit] = '1' if basis_state[target_qubit] == '0' else '0'
        # print(flipped_state)
        flipped_index = int(''.join(flipped_state), 2)
        new_state_vector[flipped_index] = state_vector[i]
    return new_state_vector


def apply_optimized_y(state_vector, target_qubit, num_qubits):
    """
    Applies the Pauli-Y gate logically to the target qubit.
    """
    new_state_vector = np.zeros_like(state_vector, dtype=complex)
    for i in range(len(state_vector)):
        basis_state = format(i, f'0{num_qubits}b')
        flipped_state = list(basis_state)
        flipped_state[target_qubit] = '1' if basis_state[target_qubit] == '0' else '0'
        flipped_index = int(''.join(flipped_state), 2)

        # Apply Pauli-Y: i or -i phase depending on the flip
        if basis_state[target_qubit] == '0':
            new_state_vector[flipped_index] += 1j * state_vector[i]
        else:
            new_state_vector[flipped_index] -= 1j * state_vector[i]
    
    # print(new_state_vector)
    
    return new_state_vector

def apply_optimized_z(state_vector, target_qubit, num_qubits):
    """
    Applies the Pauli-Z gate logically to the target qubit.
    """
    new_state_vector = np.copy(state_vector)
    for i in range(len(state_vector)):
        basis_state = format(i, f'0{num_qubits}b')
        if basis_state[target_qubit] == '1':
            new_state_vector[i] *= -1
    # print(new_state_vector)
    return new_state_vector

def apply_optimized_h(state_vector, target_qubit, num_qubits):
    """
    Correct Hadamard on target_qubit.
    Assumes `target_qubit` indexes the bitstring left-to-right (MSB = 0).
    """
    n = len(state_vector)
    new_coefficients = np.zeros_like(state_vector, dtype=complex)
    inv_sqrt2 = 1 / np.sqrt(2)

    for i in range(n):
        bitstr = format(i, f'0{num_qubits}b')
        bit = bitstr[target_qubit]
        flipped = list(bitstr)
        flipped[target_qubit] = '1' if bit == '0' else '0'
        j = int(''.join(flipped), 2)

        if bit == '0':
            new_coefficients[i] += state_vector[i] * inv_sqrt2
            new_coefficients[j] += state_vector[i] * inv_sqrt2
        else:  # bit == '1'
            new_coefficients[i] += -state_vector[i] * inv_sqrt2
            new_coefficients[j] +=  state_vector[i] * inv_sqrt2

    # print(new_coefficients)

    return new_coefficients

def apply_optimized_i(state_vector, target_qubit, num_qubits):
    """
    Applies the Identity gate logically to the target qubit (no change).
    """
    return state_vector

def apply_optimized_cnot(state_vector, control_qubit, target_qubit, num_qubits):
    """
    Applies the CNOT gate logically to the control and target qubits using separate arrays for state and coefficients.
    """
    states = np.arange(len(state_vector))
    coefficients = np.copy(state_vector)
    new_coefficients = np.zeros_like(coefficients, dtype=complex)

    for i, state in enumerate(states):
        basis_state = format(state, f'0{num_qubits}b')
        flipped_state = list(basis_state)

        if basis_state[control_qubit] == '1':
            # Flip the target qubit if the control qubit is 1
            flipped_state[target_qubit] = '1' if basis_state[target_qubit] == '0' else '0'
            flipped_index = int(''.join(flipped_state), 2)
            new_coefficients[flipped_index] = coefficients[i]
        else:
            # Keep the state unchanged if the control qubit is 0
            new_coefficients[i] = coefficients[i]

    return new_coefficients

def apply_optimized_swap(state_vector, qubit1, qubit2, num_qubits):
    """
    Applies the SWAP gate logically to the two qubits.
    """
    new_state_vector = np.zeros_like(state_vector)
    for i in range(len(state_vector)):
        basis_state = format(i, f'0{num_qubits}b')
        swapped_state = list(basis_state)
        swapped_state[qubit1], swapped_state[qubit2] = swapped_state[qubit2], swapped_state[qubit1]
        swapped_index = int(''.join(swapped_state), 2)
        new_state_vector[swapped_index] = state_vector[i]
    return new_state_vector