import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm

# Normalizing each absorbance data curve from the range [-4, 4] to [0, 1]
norm_absorbance = lambda absorbance_data: (absorbance_data + 4) * (1 / 8)

file_path = '/Users/adrian/Documents/UV-vis/Carlos_P3HT_8-22-24/Polarized Batch 4 0% Samples  - Vertical 1.csv'
df = pd.read_csv(file_path)

baseline_file_path = '/Users/adrian/Documents/UV-vis/Carlos_P3HT_8-22-24/Polarized Batch 4 0% Samples  - Baseline Vertical.csv'
baseline_df = pd.read_csv(baseline_file_path)

wavelength = df['Wavelength']
absorbance_data = df.drop(columns=['Wavelength'])
absorbance_data = absorbance_data.drop(columns=['100%']) # drop 100% because the PDMS get to narrow to completely occlude beam
normalized_absorbance_data = norm_absorbance(absorbance_data)
normalized_transmittance_data = 1 - normalized_absorbance_data

baseline_absorbance_data = baseline_df['Average']
normalized_baseline_absorbance_data = norm_absorbance(baseline_absorbance_data)
normalized_baseline_transmittance_data = 1 - normalized_baseline_absorbance_data

corrected_transmittance_data = normalized_transmittance_data.div(normalized_baseline_transmittance_data.values, axis=0)

#plotting
plt.figure(figsize=(10, 6))
colors = cm.Spectral([i / (absorbance_data.shape[1] - 1) for i in range(absorbance_data.shape[1])])

for i, column in enumerate(normalized_transmittance_data.columns): 
    plt.plot(wavelength, 1-normalized_transmittance_data[column], linestyle=':', label=f'Uncorrected Strain {column}', color=colors[i])

# Plot the corrected absorbance data with solid lines
for i, column in enumerate(corrected_transmittance_data.columns): 
    plt.plot(wavelength, 1-corrected_transmittance_data[column], label=f'Corrected Strain {column}', color=colors[i])

# Plot the baseline data in black
plt.plot(wavelength, 1-normalized_baseline_transmittance_data, label='||-Baseline', color='black', linewidth=2)

plt.title('Corrected and Uncorrected Absorbance vs. Wavelength for ||-polarized light')
plt.xlabel('Wavelength (nm)')
plt.ylabel('Absorbance')
plt.xlim((400,700))
plt.ylim((0,1))
plt.legend(title='Strain', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()