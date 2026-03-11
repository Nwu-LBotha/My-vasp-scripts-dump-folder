#!/usr/bin/python3

# Note this script requires the bader charge file (ACF), the POSCAR and the OUTCAR files. It will calculate the charges for each atom.

import pandas as pd
import re

# Function to read the atomic species and number of atoms from the POSCAR file
def read_poscar(poscar_file):
    with open(poscar_file, 'r') as file:
        lines = file.readlines()

    atom_types = lines[5].split()  # List of atomic species
    atom_counts = list(map(int, lines[6].split()))  # List of atom counts

    atoms = []
    for atom_type, count in zip(atom_types, atom_counts):
        atoms.extend([atom_type] * count)  # Create list of atoms, e.g., ['Pt', 'Pt', ..., 'Pt']

    return atom_types, atoms

# Function to read the atomic positions and properties from the ACF file
def read_acf(acf_file):
    atom_data = []
    with open(acf_file, 'r') as file:
        lines = file.readlines()

    start_reading = False
    for line in lines:
        if "--------------------------------------------------------------------------------" in line:
            start_reading = not start_reading  # Start or stop reading when this line appears
            continue
        if start_reading and line.strip() and re.match(r'\d+', line.split()[0]):
            data = list(map(float, line.split()[1:]))  # Extract atom data
            atom_data.append(data)

    return atom_data

# Function to search for ZVAL values for each element in the OUTCAR file
def get_zval(outcar_file):
    zval_dict = {}
    current_element = None

    with open(outcar_file, 'r') as file:
        lines = file.readlines()

    for line in lines:
        if "POTCAR:" in line:
            # Extract the element name
            match = re.search(r'POTCAR:\s+PAW_PBE\s+(\w+)', line)
            if match:
                current_element = match.group(1)
        if "ZVAL" in line and current_element:
            # Extract the ZVAL value for the current element
            zval_match = re.search(r'ZVAL\s+=\s+([\d\.]+)', line)
            if zval_match:
                zval = float(zval_match.group(1))  # Correctly convert the ZVAL to float
                zval_dict[current_element] = zval
                current_element = None  # Reset for the next element

    return zval_dict

# Function to assign atom types, retrieve ZVAL, and compute the corrected charge
def assign_atom_types_and_corrected_charge(acf_data, atoms, zval_dict):
    labeled_data = []
    for i, atom in enumerate(atoms):
        zval = zval_dict.get(atom, None)
        if zval is None:
            raise ValueError(f"ZVAL for atom {atom} not found in OUTCAR.")

        corrected_charge = zval - acf_data[i][3]  # ZVAL - charge
        labeled_data.append([atom, i+1] + acf_data[i] + [corrected_charge])  # Include atom index

    return labeled_data

# Function to print or save the labeled atom data with corrected charge
def print_labeled_data_with_corrected_charge(labeled_data):
    print(f"{'Atom':<5} {'Index':<5} {'X':<10} {'Y':<10} {'Z':<10} {'Charge':<10} {'Min Dist':<10} {'Atomic Vol':<10} {'Corrected Charge':<15}")
    for data in labeled_data:
        print(f"{data[0]:<5} {data[1]:<5} {data[2]:<10.4f} {data[3]:<10.4f} {data[4]:<10.4f} {data[5]:<10.4f} {data[6]:<10.4f} {data[7]:<10.4f} {data[8]:<15.4f}")

# Function to export data to an Excel file
def export_to_excel(labeled_data, filename='atom_data.xlsx'):
    # Create a DataFrame from the labeled data
    df = pd.DataFrame(labeled_data, columns=['Atom', 'Index', 'X', 'Y', 'Z', 'Charge', 'Min Dist', 'Atomic Vol', 'Corrected Charge'])

    # Export to Excel
    df.to_excel(filename, index=False)
    print(f"Data successfully exported to {filename}")

# Example usage
poscar_file = 'POSCAR'  # Replace with your POSCAR file path
acf_file = 'ACF.dat'    # Replace with your ACF file path
outcar_file = 'OUTCAR'  # Replace with your OUTCAR file path

# Read atomic data from POSCAR and ACF
atom_types, atoms = read_poscar(poscar_file)
acf_data = read_acf(acf_file)

# Get ZVAL values from OUTCAR
zval_dict = get_zval(outcar_file)

# Assign atom types, compute corrected charge, and store in labeled data
labeled_data = assign_atom_types_and_corrected_charge(acf_data, atoms, zval_dict)

# Print the labeled data with corrected charge
print_labeled_data_with_corrected_charge(labeled_data)

# Export the labeled data to Excel
export_to_excel(labeled_data)
