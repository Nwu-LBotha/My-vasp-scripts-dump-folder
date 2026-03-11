#!/usr/bin/python3

import os
from ase.io import read, write

print("=== NEB Midpoint Inserter ===")
print("Example: 2 4 will insert midpoints between 02-03 and 03-04\n")

start, end = map(int, input("Enter start and end image numbers: ").split())

for i in range(start, end):

    imgA_folder = f"{i:02d}"
    imgB_folder = f"{i+1:02d}"

    posA = os.path.join(imgA_folder, "CONTCAR")
    posB = os.path.join(imgB_folder, "CONTCAR")

    if not os.path.exists(posA) or not os.path.exists(posB):
        raise FileNotFoundError(f"CONTCAR missing in {imgA_folder} or {imgB_folder}")

    atomsA = read(posA)
    atomsB = read(posB)

    midpoint = atomsA.copy()
    midpoint.positions = (atomsA.positions + atomsB.positions) / 2

    mid_folder = f"mid_{i:02d}_{i+1:02d}"
    os.makedirs(mid_folder, exist_ok=True)

    write(os.path.join(mid_folder, "POSCAR"), midpoint, format="vasp")

    print(f"Created {mid_folder}/POSCAR")

print("\nMidpoint folders added successfully.")
