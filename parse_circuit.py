# file_parser.py

import re

def parse_circuit_file(filepath):
    """
    Reads a circuit definition file and extracts the number of qubits and instructions.
    
    Returns:
        A tuple (num_qubits, instructions_list).
    """
    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    instructions = []
    num_qubits = 0
    
    for line in lines:
        line = line.strip()
        # Ignore comments and empty lines
        if line.startswith('//') or not line:
            continue
        
        # Parse the line specifying the number of qubits
        # Case insensitive match for "circuit: N qubits"
        # Example: "circuit: 3 qubits"
        if line.lower().startswith('circuit:'):
            match = re.search(r'circuit:\s*(\d+)\s*qubits', line, re.IGNORECASE)
            if match:
                num_qubits = int(match.group(1))
        
        # Parse the measurement instruction.
        # Accepts either "measure <idx>" or "measure <start>..<end>" (inclusive).
        elif line.lower().startswith('measure'):
            parts = line.split()
            if len(parts) < 2:
                raise ValueError(f"Malformed measure instruction: '{line}'. Expected 'measure <idx>' or 'measure <start>..<end>'.")

            target = parts[1]
            if '..' in target:
                bounds = target.split('..')
                if len(bounds) != 2 or not bounds[0] or not bounds[1]:
                    raise ValueError(f"Malformed measure range: '{line}'. Use 'measure a..b'.")
                start, end = int(bounds[0]), int(bounds[1])
            else:
                start = end = int(target)

            if start < 0 or end < start:
                raise ValueError(f"Invalid measure range in line: '{line}' (start={start}, end={end}).")

            instructions.append(('measure', list(range(start, end + 1))))
        
        # Parse gate instructions (e.g., "H(0)" or "CNOT(0,2)")
        # Case insensitive match for gate instructions
        else:
            match = re.match(r'(\w+)\(([\d,]+)\)', line) 
            if match:
                gate_name = match.group(1).upper()
                qubits = [int(q) for q in match.group(2).split(',')] 
                instructions.append((gate_name, qubits)) 
    
        # print(f"Parsed line: '{line}' -> {instructions[-1] if instructions else 'Not an instruction'}") 
        
    return num_qubits, instructions