#!/apps/chpc/chem/anaconda3-2019.10/bin/python


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


# Load the data from the file, assuming the file has two columns: x and y
data = np.loadtxt(file_path)

# Split the data into two separate arrays: x (first column) and y (second column)
x = data[:, 0]
y = data[:, 1]

# Calculate the total area under the curve using the trapezoidal rule
total_area = np.trapz(y, x)

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
plt.fill_between(x, y, color='skyblue', alpha=0.4, label=f'Area = {total_area:.2f}')

# Mark the point where the area is half of the total area
plt.axvline(x=x_half_area, color='red', linestyle='--', label=f'd-band centre ≈ {x_half_area:.2f}')

# Add labels and title
plt.xlabel('E (eV)')
plt.ylabel('DOS')
plt.title('PDOS')

# Show the legend
plt.legend()

#Save the plot
plt.savefig('d-band centre.png')

# Display the plot
plt.show()

# Print the total area and the x-coordinate where area = half_area
print(f"The total area under the curve is: {total_area}")
print(f"The d-band centre is : {x_half_area}")

#df_selected.to_csv(file_path + 'd-band-data.csv', sep=',', index=False, encoding='utf-8')



#
# Dr Louise M Botha
