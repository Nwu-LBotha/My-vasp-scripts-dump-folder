#!/apps/chpc/chem/anaconda3-2019.10/bin/python

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re

# Define the file path
file_path = 'OUTCAR'

# Initialize lists to store vacuum levels and E-fermi value
upper_vacuum = []
lower_vacuum = []
e_fermi = None

# Open and read the OUTCAR file
with open(file_path, 'r') as file:
    for line in file:
        # Search for lines containing "vacuum level on the upper side and lower side"
        if "vacuum level on the upper side and lower side of the slab" in line:
            # Use regular expressions to extract the upper and lower vacuum levels
            match = re.findall(r"[-+]?\d*\.\d+|\d+", line)
            if match and len(match) == 2:
                upper_vacuum.append(float(match[0]))
                lower_vacuum.append(float(match[1]))

        # Search for lines containing "E-fermi"
        if "E-fermi" in line:
            # Use regular expressions to extract the E-fermi value
            match = re.search(r"E-fermi\s*:\s*([-+]?\d*\.\d+)", line)
            if match:
                e_fermi = float(match.group(1))

# Calculate the work function if both the upper vacuum level and E-fermi are found
if upper_vacuum and e_fermi is not None:
    # Subtract E-fermi from the upper vacuum level to calculate the work function
    work_function = [vacuum - e_fermi for vacuum in upper_vacuum]
    print("Lower vacuum levels:", lower_vacuum)
    print(f"Upper vacuum levels: {upper_vacuum}")
    print(f"E-fermi value: {e_fermi}")
    print(f"Work function: {work_function}")
else:
    print("Data not sufficient to calculate the work function.")

#
# Louise M Botha
