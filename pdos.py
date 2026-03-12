#!/apps/chpc/chem/anaconda3-2019.10/bin/python

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#file_path = "PDOS_Pt_UP.dat"
#PLease note, this script is for the full DOS and not the PDOS.
#Since the vaspkit and qvasp toolkits can give more than one file, we will rather let the user choose their file.

x = input('Enter a file name: ')

try:
    with open(x) as f:
        data = f.readlines()
    for i in range(5):
        print(data[i])
except:
    print('No such a file found!')

# The selected file is specified with the identifier file path
file_path = x

# Load the data, skipping the first comment line (the #headers)
columns = ['Energy', 's', 'py', 'pz', 'px', 'dxy', 'dyz', 'dz2', 'dxz', 'dx2', 'tot']
df = pd.read_csv(file_path, sep='\s+', comment='#', names=columns)

# Select only the 'Energy', 'dxy', 'dyz', 'dz2', 'dxz', and 'dx2' columns
df_selected = df.loc[:, ['Energy', 'dxy', 'dyz', 'dz2', 'dxz', 'dx2']]

# Add a new column that sums the values of 'dxy', 'dyz', 'dz2', 'dxz', and 'dx2'
df_selected['Sum'] = df_selected[['dxy', 'dyz', 'dz2', 'dxz', 'dx2']].sum(axis=1)
#print(df_selected)

#df_selected.to_csv(file_path + 'pdos_data.csv', sep=',', index=False, encoding='utf-8')

#Export the dataframe to an excel file

#We will create a new dataframe with only the d-band. There are a number of rows that are zero values so we need to only use the non-zero values to determine the area.

df_non_zero_sum = df_selected[df_selected['Sum'] != 0].dropna(subset=['Energy', 'Sum'])

# Extract Energy and Sum columns as x and y
x = df_non_zero_sum['Energy'].values
y = df_non_zero_sum['Sum'].values

# Calculate the total area under the curve
total_area = np.trapz(y, x)
#print("Total Area:", total_area)

# Calculate half of the total area
half_area = total_area / 2

# Initialize the cumulative area array
cumulative_area = np.zeros_like(x)

# Compute cumulative area at each point using the trapezoidal rule
for i in range(1, len(x)):
    cumulative_area[i] = np.trapz(y[:i+1], x[:i+1])

# Find the x-value where the cumulative area is closest to half of the total area
idx = np.abs(cumulative_area - half_area).argmin()
x_half_area = x[idx]

# Plot the data points and the area under the curve
plt.figure(figsize=(10, 6))
plt.plot(x, y, label="d-band", color='blue')

# Fill the area under the curve
#plt.fill_between(x, y, color='skyblue', alpha=0.4, label=f'Area = {total_area:.2f}')

plt.fill_between(x, y, where=(x >= 0), color='red', alpha=0.5, label='Conduction band')
plt.fill_between(x, y, where=(x < 0), color='skyblue', alpha=0.5, label='Valence band')

# Mark the point where the area is half of the total area
plt.axvline(x=x_half_area, color='red', linestyle='--', label=f'd-band centre ≈ {x_half_area:.2f}')

# Add a vertical line at x = 0 and label it as "Fermi Level"
plt.axvline(x=0, color='black', linestyle='--', linewidth=1.5, label='Fermi Level')

# Add labels and title
plt.xlabel('E (eV)')
plt.ylabel('PDOS')
plt.title('Projected d-band centre')

# Show the legend
plt.legend()

# save the image
plt.savefig('d-band centre.png')

# Display the plot
plt.show()

# Print the total area and the x-coordinate where area = half_area
print(f"The total area under the curve is: {total_area}")
print(f"The d-band centre is : {x_half_area}")

print("By Louise M Botha, ORCID: https://orcid.org/0000-0002-1249-2706")
