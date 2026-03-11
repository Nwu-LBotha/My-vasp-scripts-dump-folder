#!/apps/chpc/chem/anaconda3-2019.10/bin/python


import numpy as np
import matplotlib.pyplot as plt

import re

def extract_volume_and_vectors(outcar_file, output_file):
    volume = None
    vector_lengths = None

    with open(outcar_file, 'r') as file:
        for line in file:
            if "volume of cell" in line:
                volume = float(line.split(":")[1].strip())  # Extract volume value

            if "length of vectors" in line:
                vector_lengths = list(map(float, line.split()[3:6]))  # Extract vector lengths

    # Save the extracted values to a text file
    if volume is not None and vector_lengths is not None:
        with open(output_file, "w") as out_file:
            out_file.write(f"Volume of cell: {volume}\n")
            out_file.write(f"Length of vectors: {vector_lengths[0]}, {vector_lengths[1]}, {vector_lengths[2]}\n")
        print(f"Output saved to {output_file}")
    else:
        print("Could not find the required data in OUTCAR.")

# Example usage
outcar_file = "OUTCAR"   # Ensure this file exists in the same directory
output_file = "lattice_paramaters.txt"  # Name of the output file

extract_volume_and_vectors(outcar_file, output_file)

#DR Louise Botha
