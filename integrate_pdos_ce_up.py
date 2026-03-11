#!/apps/chpc/chem/anaconda3-2019.10/bin/python

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the PDOS file (skip first comment line with #)
df = pd.read_csv("PDOS_CE_UP.dat", delim_whitespace=True, comment="#", header=None)

# Re-read with header line
with open("PDOS_CE_UP.dat") as f:
    header = f.readline().strip().lstrip("#").split()

# Assign proper column names
df.columns = header

# Extract energy and f-orbital columns
energy = df["Energy"]
f_columns = [col for col in df.columns if col.startswith("f")]
ce_4f_total = df[f_columns].sum(axis=1)

# Optional: You can load O 2p data the same way from a PDOS_O_UP.dat if available
# Here we simulate that O 2p max is at -34.95 eV (manually adjust based on your data)
valence_max = -34.95

# Find the first energy where Ce 4f starts rising (onset)
threshold = 0.1
conduction_min = energy[(energy > valence_max) & (ce_4f_total > threshold)].min()

# Integrate Ce 4f in the band gap
mask = (energy > valence_max) & (energy < conduction_min)
ce_4f_gap_integrated = np.trapz(ce_4f_total[mask], energy[mask])

# Print result
print(f"\n✅ Integrated Ce 4f states in the gap: {ce_4f_gap_integrated:.4f} a.u.")
print(f"   Energy window: {valence_max:.2f} eV to {conduction_min:.2f} eV")

# Plot Ce 4f PDOS
plt.figure(figsize=(10, 5))
plt.plot(energy, ce_4f_total, label="Ce 4f", color='purple')
plt.axvline(valence_max, linestyle='--', color='gray', label='VBM (O 2p)')
plt.axvline(conduction_min, linestyle='--', color='red', label='CBM (Ce 4f)')
plt.xlabel("Energy (eV)")
plt.ylabel("DOS (a.u.)")
plt.title("Ce 4f PDOS")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
