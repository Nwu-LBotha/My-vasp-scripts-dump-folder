#!/apps/chpc/chem/anaconda3-2019.10/bin/python

from pymatgen.io.vasp.outputs import Doscar
import numpy as np
import matplotlib.pyplot as plt

# Load the DOSCAR file
doscar = Doscar("DOSCAR")

# Set up parameters
efermi = doscar.efermi
energies = np.array(doscar.tdos.energies) - efermi  # Shift energies

# Estimate total DOS
tdos = doscar.tdos.densities[Spin.up]  # or average over spins if needed

# Get partial DOS
partial_dos = doscar.pdos

# ----- MANUAL INPUT -----
# Adjust indices according to your structure (0-based)
ce_indices = [0, 1]  # e.g., atoms 1 and 2 are Ce
o_indices = [2, 3, 4, 5]  # e.g., atoms 3-6 are O

# Orbital mappings (string or index)
# Usually orbitals = ['s', 'p', 'd', 'f']
# But check doscar.orbital_data.keys() for actual labels
target_orbital_Ce = 'f'
target_orbital_O = 'p'

# Accumulate PDOS
ce_4f_total = np.zeros_like(energies)
o_2p_total = np.zeros_like(energies)

for site_index, site_dos in partial_dos.items():
    if site_index in ce_indices:
        ce_4f_total += site_dos[target_orbital_Ce][Spin.up]
    elif site_index in o_indices:
        o_2p_total += site_dos[target_orbital_O][Spin.up]

# Determine band gap region
threshold = 0.1
max_o_energy = max(energies[o_2p_total > threshold])
min_ce_energy = min(energies[(energies > max_o_energy) & (ce_4f_total > threshold)])

# Integrate Ce 4f in the gap
mask = (energies > max_o_energy) & (energies < min_ce_energy)
area_ce_4f_gap = np.trapz(ce_4f_total[mask], energies[mask])

# Print result
print(f"Integrated Ce 4f DOS in gap: {area_ce_4f_gap:.3f} a.u.")

# Optional plot
plt.figure(figsize=(10, 5))
plt.plot(energies, o_2p_total, label="O 2p")
plt.plot(energies, ce_4f_total, label="Ce 4f")
plt.axvline(max_o_energy, color='gray', linestyle='--', label='O 2p max')
plt.axvline(min_ce_energy, color='red', linestyle='--', label='Ce 4f min')
plt.xlabel("Energy (eV, E - E_F)")
plt.ylabel("DOS (a.u.)")
plt.title("Partial DOS from DOSCAR")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
