# simulator.py

import argparse
from parse_circuit import parse_circuit_file
from quantum_circuit import QC

def main():
    """ Main function to run the simulator from the command line. """
    parser = argparse.ArgumentParser(description="Quantum Circuit Simulator")
    parser.add_argument('filepath', type=str, help="Path to the circuit input file.")
    
    # Mutually exclusive group (requires either -noiseless or -noise)
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument('-noiseless', action='store_true', help="Run in noiseless mode.")
    mode_group.add_argument('-noise', action='store_true', help="Run in noisy mode.")
    
    parser.add_argument('-error', type=float, default=0.01, help="Bit-flip error probability for noisy mode.")
    parser.add_argument('-optimize', action='store_true', help="Use optimized logical operations")
    
    args = parser.parse_args()
    
    # Determine if optimized operations should be used
    optimized = args.optimize

    try:
        # 1. Parse the input file
        num_qubits, instructions = parse_circuit_file(args.filepath)
        if num_qubits == 0:
            print("Error: Number of qubits not specified in the circuit file.")
            return

        # 2. Initialize the quantum circuit
        circuit = QC(num_qubits) 
        noise_prob = args.error if args.noise else 0.0
        
        print(f"--- Starting Quantum Simulation ---")
        print(f"Mode: {'Noisy' if args.noise else 'Noiseless'}")
        if args.noise:
            print(f"Error Probability: {noise_prob}")
        print(f"Qubits: {num_qubits}\n")
        
        measurement_result = None
        
        # 3. Execute instructions one by one
        for instruction in instructions:
            op_name, qubits = instruction
            if op_name == 'measure':
                print(f"\nMeasuring qubits {qubits}...")
                measurement_result = circuit.measure(qubits)
                break # Stop simulation after the first measurement
            else:
                circuit.apply_gate(op_name, qubits, noise_prob, optimized=optimized)
        
        # 4. Print the final result
        if measurement_result is not None:
            print("\n--- Simulation Complete ---")
            print(f"Final Measurement Result for qubits {qubits}: {measurement_result}")
        else:
            pass
            # print("\nWarning: No measurement instruction found in the circuit.")

    except FileNotFoundError:
        print(f"Error: The file '{args.filepath}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()