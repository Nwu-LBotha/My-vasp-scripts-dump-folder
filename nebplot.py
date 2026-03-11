#!/usr/bin/python3

import pandas as pd
import matplotlib.pyplot as plt

# Load the data (space-delimited, no header)
data = pd.read_csv("nebenergies.txt", sep=r"\s+", header=None)

# Extract columns
images = data[0]
raw_energies = data[2]       # absolute energies
rel_energies = data[3]       # relative (transition state) energies

# Shift both curves so minimum = 0
raw_energies -= raw_energies.min()
rel_energies -= raw_energies.min()

# Plot
plt.figure(figsize=(7,5))
plt.plot(images, raw_energies, marker='o', linestyle='-', color='b', label="NEB energies")
plt.plot(images, rel_energies, marker='o', linestyle='--', color='r', label="Relative TS energies")

# Labels
plt.xlabel("Images", fontsize=12)
plt.ylabel("Energy (eV)", fontsize=12)
plt.title("NEB Energy Profile", fontsize=14)
plt.legend()

# Grid
plt.grid(True, linestyle='--', alpha=0.6)

# Save and show
plt.savefig("neb_profile.png", dpi=300, bbox_inches="tight")
plt.show()
