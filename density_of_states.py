#!/apps/chpc/chem/anaconda3-2019.10/bin/python


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


x = input('Enter a file name: ')
try:
    with open(x) as f:
        data = f.readlines()
    for i in range(5):
        print(data[i])
except:
    print('No such a file found!')


# Specify the file path
#file_path = 'PDOS_Pt_UP.dat'
file_path = x

# Specify the file path
#file_path = 'PDOS_Pt_UP.dat'

# Load the data, skipping the first comment line (header with #)
columns = ['Energy', 's', 'py', 'pz', 'px', 'dxy', 'dyz', 'dz2', 'dxz', 'dx2', 'tot']
df = pd.read_csv(file_path, sep='\s+', comment='#', names=columns)

# Select only the 'Energy', 'dxy', 'dyz', 'dz2', 'dxz', and 'dx2' columns
df_selected = df.loc[:, ['Energy', 'dxy', 'dyz', 'dz2', 'dxz', 'dx2']]

# Add a new column that sums the values of 'dxy', 'dyz', 'dz2', 'dxz', and 'dx2'
df_selected['Sum'] = df_selected[['dxy', 'dyz', 'dz2', 'dxz', 'dx2']].sum(axis=1)

# Display the resulting DataFrame
print(df_selected)

df_selected.to_csv(file_path + '.csv', sep=',', index=False, encoding='utf-8')

# Plotting
plt.figure(figsize=(8, 6))
plt.plot(df_selected['Sum'], df_selected['Energy'], linestyle='-', color='b')
#plt.plot(df_selected['Sum'], df_selected['Energy'], marker='o', linestyle='-', color='b')
plt.xlabel('PDOS')
plt.ylabel('Energy [eV]')
plt.title('Partial density of states')

# Set custom y-axis limits
plt.ylim(-20, 20)  # Set min and max for y-axis

plt.grid(True)
plt.show()

#
# Dr Louise M Botha
#
