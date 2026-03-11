#!/usr/bin/python3

from ase.io import read
from ase.io.bader import attach_charges
import pandas as pd

# Read atoms from POSCAR
atoms = read("POSCAR")

# Attach Bader charges from ACF.dat
attach_charges(atoms, 'ACF.dat')

# Store data for export
labeled_data = []

# Print and collect Bader charges
for i, atom in enumerate(atoms):
    charge = atom.charge
    print(f"Atom {i:3d}  {atom.symbol:2s}  Bader charge = {charge:8.4f}")
    labeled_data.append([i, atom.symbol, charge])


# Function to export data to an Excel file
def export_to_excel(labeled_data, filename='bader_energy_data.xlsx'):
    # Create a DataFrame from the labeled data
    df = pd.DataFrame(labeled_data,
                      columns=['Atom', 'Symbol', 'Bader charge'])

    # Export to Excel
    df.to_excel(filename, index=False)
    print(f"Data successfully exported to {filename}")


# Export the labeled data to Excel
export_to_excel(labeled_data)

#Dr Louise M Botha

