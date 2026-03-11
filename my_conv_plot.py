#!/usr/bin/python3

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import subprocess

# Step 1: Extract TOTEN values from OUTCAR
try:
    subprocess.run('grep "TOTEN" OUTCAR > energies.txt', shell=True, check=True)
    print("TOTEN values extracted to 'energies.txt'")
except subprocess.CalledProcessError:
    print("Error: Failed to extract TOTEN values. Check that OUTCAR exists.")
    exit()

# Step 2: Read and parse the TOTEN energy values
file_path = 'energies.txt'
free_energy_values = []

with open(file_path, 'r') as file:
    for line in file:
        if 'TOTEN' in line:
            try:
                energy_value = float(line.split('=')[-1].strip().split()[0])
                free_energy_values.append(energy_value)
            except ValueError:
                print(f"Warning: Could not parse energy from line: {line.strip()}")

# Step 3: Create DataFrame
df = pd.DataFrame(free_energy_values, columns=['Free Energy (TOTEN) [eV]'])
df['Row'] = df.index + 1
df_selected = df[['Row', 'Free Energy (TOTEN) [eV]']]

# Step 4: Save DataFrame to CSV
df_selected.to_csv('data_energies.csv', sep=',', index=False, encoding='utf-8')
print("Data saved to 'data_energies.csv'.")

# Step 5: Suggest axis limits based on data
x_min_suggested = df_selected['Row'].min()
x_max_suggested = df_selected['Row'].max()
y_min_suggested = df_selected['Free Energy (TOTEN) [eV]'].min() - 10
y_max_suggested = df_selected['Free Energy (TOTEN) [eV]'].max() + 10

print("\n--- Axis Limits ---")
try:
    x_min = input(f"Enter minimum x-axis value (>= {x_min_suggested}): ")
    x_min = int(x_min) if x_min.strip() else x_min_suggested

    x_max = input(f"Enter maximum x-axis value (<= {x_max_suggested}): ")
    x_max = int(x_max) if x_max.strip() else x_max_suggested

    y_min = input(f"Enter minimum y-axis value (>= {y_min_suggested:.2f}): ")
    y_min = float(y_min) if y_min.strip() else y_min_suggested

    y_max = input(f"Enter maximum y-axis value (<= {y_max_suggested:.2f}): ")
    y_max = float(y_max) if y_max.strip() else y_max_suggested

except ValueError:
    print("Invalid input. Please enter numeric values.")
    exit()

# Step 6: Plotting
plt.figure(figsize=(8, 6))
plt.plot(df_selected['Row'], df_selected['Free Energy (TOTEN) [eV]'],
         marker='o', linestyle='-', color='b', label='TOTEN')

plt.xlabel('Step (Row)')
plt.ylabel('Free Energy (TOTEN) [eV]')
plt.title('VASP Energy Convergence')
plt.grid(True)
plt.legend()

# Apply axis limits
plt.xlim(x_min, x_max)
plt.ylim(y_min, y_max)

# Save the figure
plt.tight_layout()
plt.savefig('energy_convergence.png', dpi=300)
print("Plot saved as 'energy_convergence.png'.")

# Show the plot
plt.show()

#Dr Louise M Botha
