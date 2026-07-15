#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import numpy as np
from ase.io import read

print("=== NEB Bond Analysis v5 (Indexed + Generic) ===")

neb_path = input("NEB folder (default = .): ") or "."
max_images = 50

# -------------------------------
# USER INPUT
# -------------------------------
print("\nEnter bonds to track:")
print("Examples:")
print("  O-H           (tracks all O-H bonds)")
print("  O16-H18       (tracks specific atoms)")
print("  O16-H18, O17-H19, Pt-O")

pairs_input = input("Enter pairs separated by commas: ")
pairs_raw = [p.strip() for p in pairs_input.split(",")]

max_distance = float(input("Enter max bond distance (Å, default=2.5): ") or 2.5)

# -------------------------------
# Bond thresholds (Å)
# -------------------------------
bond_limits = {
    ("O", "O"): (1.2, 1.6),
    ("O", "H"): (0.9, 1.2),
    ("Pt", "O"): (1.8, 2.3),
    ("Pt", "H"): (1.5, 2.0)
}

# -------------------------------
# Helpers
# -------------------------------

def find_images(path):
    images = []
    for i in range(max_images):
        folder = os.path.join(path, f"{i:02d}")
        if os.path.exists(folder):
            for f in ["CONTCAR", "POSCAR"]:
                fpath = os.path.join(folder, f)
                if os.path.exists(fpath):
                    images.append((i, fpath))
                    break
    return images

def get_indices(atoms, symbol):
    return [i for i, a in enumerate(atoms) if a.symbol == symbol]

def parse_pair(pair):
    # Detect indexed vs generic
    if any(char.isdigit() for char in pair):
        A, B = pair.split("-")
        symA = ''.join(filter(str.isalpha, A))
        idxA = int(''.join(filter(str.isdigit, A))) - 1
        symB = ''.join(filter(str.isalpha, B))
        idxB = int(''.join(filter(str.isdigit, B))) - 1
        return ("indexed", pair, symA, idxA, symB, idxB)
    else:
        A, B = pair.split("-")
        return ("generic", pair, A, B)

# -------------------------------
# Load NEB images
# -------------------------------

images = find_images(neb_path)
if not images:
    raise RuntimeError("No NEB images found!")

print("\n=== Distance Analysis ===\n")

results = []
bond_history = {}

# initialize history
for p in pairs_raw:
    bond_history[p] = []

# -------------------------------
# Main Loop
# -------------------------------

for idx, filepath in images:

    atoms = read(filepath)
    row = [f"Image {idx:02d}"]

    for pair in pairs_raw:

        parsed = parse_pair(pair)

        # -----------------------
        # Indexed pair
        # -----------------------
        if parsed[0] == "indexed":
            _, label, symA, ia, symB, ib = parsed
            d = atoms.get_distance(ia, ib, mic=True)

            row.append(f"{label}:{d:.3f}")
            bond_history[pair].append(d)

        # -----------------------
        # Generic pair
        # -----------------------
        else:
            _, label, A, B = parsed
            idxA = get_indices(atoms, A)
            idxB = get_indices(atoms, B)

            distances = []
            min_dist = None

            for i, ia in enumerate(idxA, start=1):
                for j, ib in enumerate(idxB, start=1):
                    if ia != ib:
                        d = atoms.get_distance(ia, ib, mic=True)

                        if (min_dist is None) or (d < min_dist):
                            min_dist = d

                        if d <= max_distance:
                            distances.append(f"{A}{i}-{B}{j}:{d:.3f}")

            if distances:
                row.append(", ".join(distances))
            else:
                row.append("---")

            bond_history[pair].append(min_dist if min_dist else np.nan)

    results.append(row)

    # print
    print(f"{row[0]:8s} ", end="")
    for val in row[1:]:
        print(f"| {val}", end=" ")
    print()

# -------------------------------
# Save full data
# -------------------------------

with open("bond_analysis_full.dat", "w") as f:
    header = "Image " + " ".join(pairs_raw)
    f.write(header + "\n")
    for r in results:
        f.write(r[0] + " " + " ".join([x if x != "---" else "nan" for x in r[1:]]) + "\n")

print("\n✔ Saved detailed distances to bond_analysis_full.dat")

# -------------------------------
# Bond evolution classification
# -------------------------------

print("\n=== Bond Formation / Breaking Analysis ===\n")

summary = []

for pair, dist_list in bond_history.items():

    parsed = parse_pair(pair)

    if parsed[0] == "indexed":
        _, _, A, _, B, _ = parsed
    else:
        _, _, A, B = parsed

    # handle reversed pairs
    if (A, B) in bond_limits:
        key = (A, B)
    elif (B, A) in bond_limits:
        key = (B, A)
    else:
        key = None

    if key:
        dmin, dmax = bond_limits[key]
    else:
        dmin, dmax = (0.0, max_distance)

    start = dist_list[0]
    end = dist_list[-1]

    if np.isnan(start) or np.isnan(end):
        status = "UNCLEAR"

    elif start > dmax and end < dmax:
        status = "FORMING"

    elif start < dmax and end > dmax:
        status = "BREAKING"

    elif abs(end - start) < 0.1:
        status = "STABLE"

    else:
        status = "REARRANGING"

    summary.append((pair, start, end, status))

# -------------------------------
# Print summary
# -------------------------------

print(f"{'Bond':15s} {'Start (Å)':>12s} {'End (Å)':>12s} {'Status':>12s}")

for b, s, e, st in summary:
    print(f"{b:15s} {s:12.3f} {e:12.3f} {st:12s}")

# -------------------------------
# Save summary
# -------------------------------

with open("bond_evolution_summary.dat", "w") as f:
    f.write("Bond Start(Å) End(Å) Status\n")
    for b, s, e, st in summary:
        f.write(f"{b} {s:.3f} {e:.3f} {st}\n")

print("\n✔ Saved bond evolution summary to bond_evolution_summary.dat")