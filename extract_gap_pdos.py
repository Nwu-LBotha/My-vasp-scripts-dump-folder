#!/apps/chpc/chem/anaconda3-2019.10/bin/python

from pymatgen.io.vasp import Vasprun
import numpy as np
import matplotlib.pyplot as plt

# Load the vasprun.xml file
vasprun = Vasprun("vasprun.xml", parse_projected=True)
complete_dos = vasprun.complete_dos

# Extract Fermi energy
e_fermi = vasprun.efermi

# Get energy and Ce 4f and O 2p PDOS
energies = complete_dos.energies - e_fermi  # shift relative to E_F
pdos = complete_dos.pdos

# Initialize totals
ce_4f_total = np.zeros(len(energies))
o_2p_total = np.zeros(len(energies))

# Loop through all sites
for site, pdos_dict in zip(complete_dos.structure, pdos):
    if "Ce" in str(site.specie):
        ce_4f_total += np.sum(pdos_dict["4f"], axis=0)
    elif "O" in str(site.specie):
        o_2p_total += np.sum(pdos_dict["2p"], axis=0)

# Identify top of O 2p (valence band max) and bottom of Ce 4f (conduction band min)
threshold = 0.1
max_o_energy = max(energies[o_2p_total > threshold])
min_ce_energy = min(energies[(energies > max_o_energy) & (ce_4f_total > threshold)])

# Filter Ce 4f in the gap region
mask = (energies > max_o_energy) & (energies < min_ce_energy)
gap_integrated_ce_4f = np.trapz(ce_4f_total[mask], energies[mask])

print(f"Integrated Ce 4f states in the gap: {gap_integrated_ce_4f:.3f} a.u.")

# Optional plot
plt.figure(figsize=(10, 5))
plt.plot(energies, o_2p_total, label="O 2p")
plt.plot(energies, ce_4f_total, label="Ce 4f")
plt.axvline(max_o_energy, color="gray", linestyle="--", label="O 2p max")
plt.axvline(min_ce_energy, color="red", linestyle="--", label="Ce 4f min")
plt.xlabel("Energy (eV, E - E_F)")
plt.ylabel("DOS (a.u.)")
plt.title("Projected DOS: O 2p and Ce 4f")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
