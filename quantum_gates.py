# quantum_gates.py

import numpy as np # type: ignore

# --- Basic Gate Matrix Definitions ---
I = np.identity(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)
H = (1 / np.sqrt(2)) * np.array([[1, 1], [1, -1]], dtype=complex)
SWAP = np.array([[1, 0, 0, 0],
                 [0, 0, 1, 0],
                 [0, 1, 0, 0],
                 [0, 0, 0, 1]], dtype=complex)


def get_operator(gate_name, qubits, num_qubits):
    """
    Factory function to get the appropriate operator for a given gate.
    
    Parameters:
        gate_name (str): Name of the gate ('H', 'X', 'Y', 'Z', 'I', 'CNOT', 'SWAP')
        qubits (list): Qubit indices for the gate
        num_qubits (int): Total number of qubits in the system
    
    Returns:
        np.ndarray: The operator matrix for the gate, or None if gate not recognized
    """
    if gate_name == 'H':
        return get_single_qubit_operator(H, qubits[0], num_qubits)
    elif gate_name == 'X':
        return get_single_qubit_operator(X, qubits[0], num_qubits)
    elif gate_name == 'Y':
        return get_single_qubit_operator(Y, qubits[0], num_qubits)
    elif gate_name == 'Z':
        return get_single_qubit_operator(Z, qubits[0], num_qubits)
    elif gate_name == 'I':
        return get_single_qubit_operator(I, qubits[0], num_qubits)
    elif gate_name == 'CNOT':
        return get_cnot_operator(qubits[0], qubits[1], num_qubits)
    elif gate_name == 'SWAP':
        return get_swap_operator(qubits[0], qubits[1], num_qubits)
    else:
        return None


def get_single_qubit_operator(gate_matrix, target_qubit, num_qubits):
    """
    Constructs the full 2^n x 2^n operator matrix for a single-qubit gate
    by applying it to the target qubit and using identity for all others.
    """
    op_list = [I] * num_qubits
    op_list[target_qubit] = gate_matrix
    
    # Combine all matrices using the tensor product (np.kron)
    full_op = op_list[0]
    for i in range(1, num_qubits):
        full_op = np.kron(full_op, op_list[i])
        
    return full_op

def get_cnot_operator(control_qubit, target_qubit, num_qubits):
    """
    Constructs the full 2^n x 2^n CNOT operator matrix.
    
    This works by iterating through each basis state and determining
    where it maps to. If the control bit is 1, the target bit is flipped.
    """
    num_states = 2**num_qubits
    cnot_op = np.zeros((num_states, num_states), dtype=complex)
    
    for i in range(num_states):
        # Convert the state's index to a binary string
        basis_state = format(i, f'0{num_qubits}b')
        
        # If the control bit is '1', flip the target bit
        if basis_state[control_qubit] == '1':
            flipped_state_list = list(basis_state)
            flipped_state_list[target_qubit] = '1' if basis_state[target_qubit] == '0' else '0'
            flipped_state = "".join(flipped_state_list)
            # Find the index of the resulting state
            j = int(flipped_state, 2)
            cnot_op[j, i] = 1 # Map input state 'i' to output state 'j'
        else:
            # If control bit is '0', the state is unchanged
            cnot_op[i, i] = 1
            
    return cnot_op

def get_swap_operator(qubit1, qubit2, num_qubits):
    """
    Constructs the full 2^n x 2^n SWAP operator matrix.
    """
    num_states = 2**num_qubits
    swap_op = np.zeros((num_states, num_states), dtype=complex)
    
    for i in range(num_states):
        basis_state = format(i, f'0{num_qubits}b')
        
        # Swap the bits at qubit1 and qubit2
        swapped_state_list = list(basis_state)
        swapped_state_list[qubit1], swapped_state_list[qubit2] = swapped_state_list[qubit2], swapped_state_list[qubit1]
        swapped_state = "".join(swapped_state_list)
        
        j = int(swapped_state, 2)
        swap_op[j, i] = 1 # Map input state 'i' to output state 'j'
        
    return swap_op

