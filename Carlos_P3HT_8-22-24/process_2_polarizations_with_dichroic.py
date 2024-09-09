import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm

# utility Function to normalize each absorbance data curve from the range [-4, 4] to [0, 1]
norm_absorbance = lambda absorbance_data: (absorbance_data + 4) * (1 / 8)

date = "2024-08-22"  # Replace with desired date for plot title

# get files
s_num = 2
vertical_file_path = f'/Users/adrian/Documents/UV-vis/Carlos_P3HT_8-22-24/Polarized Batch 4 0% Samples  - Vertical {s_num}.csv'
horizontal_file_path = f'/Users/adrian/Documents/UV-vis/Carlos_P3HT_8-22-24/Polarized Batch 4 0% Samples  - Horizontal {s_num}.csv'
baseline_vertical_file_path = '/Users/adrian/Documents/UV-vis/Carlos_P3HT_8-22-24/Polarized Batch 4 0% Samples  - Baseline Vertical.csv'
baseline_horizontal_file_path = '/Users/adrian/Documents/UV-vis/Carlos_P3HT_8-22-24/Polarized Batch 4 0% Samples  - Baseline Horizontal.csv'

#loaod data
vertical_df = pd.read_csv(vertical_file_path)
baseline_vertical_df = pd.read_csv(baseline_vertical_file_path)
horizontal_df = pd.read_csv(horizontal_file_path)
baseline_horizontal_df = pd.read_csv(baseline_horizontal_file_path)

# process vertical polarized data
wavelength = vertical_df['Wavelength']
vertical_absorbance_data = vertical_df.drop(columns=['Wavelength'])
vertical_absorbance_data = vertical_absorbance_data.drop(columns=['100%'])
normalized_vertical_absorbance_data = norm_absorbance(vertical_absorbance_data)
normalized_vertical_transmittance_data = 1 - normalized_vertical_absorbance_data

baseline_vertical_absorbance_data = baseline_vertical_df['Average']
normalized_baseline_vertical_absorbance_data = norm_absorbance(baseline_vertical_absorbance_data)
normalized_baseline_vertical_transmittance_data = 1 - normalized_baseline_vertical_absorbance_data

#apply correction by dividing combined transmittance by transmittance of pure polarixer
corrected_vertical_transmittance_data = normalized_vertical_transmittance_data.div(normalized_baseline_vertical_transmittance_data.values, axis=0)

#process horizontal polarized data, same as verticle
horizontal_absorbance_data = horizontal_df.drop(columns=['Wavelength'])
horizontal_absorbance_data = horizontal_absorbance_data.drop(columns=['100%'])
normalized_horizontal_absorbance_data = norm_absorbance(horizontal_absorbance_data)
normalized_horizontal_transmittance_data = 1 - normalized_horizontal_absorbance_data

baseline_horizontal_absorbance_data = baseline_horizontal_df['Average']
normalized_baseline_horizontal_absorbance_data = norm_absorbance(baseline_horizontal_absorbance_data)
normalized_baseline_horizontal_transmittance_data = 1 - normalized_baseline_horizontal_absorbance_data

corrected_horizontal_transmittance_data = normalized_horizontal_transmittance_data.div(normalized_baseline_horizontal_transmittance_data.values, axis=0)

# convert to absorbance
corrected_horizontal_absorbance_data = 1-corrected_horizontal_transmittance_data
corrected_vertical_absorbance_data = 1 - corrected_vertical_transmittance_data

# Calculate the dichroic ratio
dichroic_ratio_T = corrected_vertical_transmittance_data.div(corrected_horizontal_transmittance_data.values, axis=0)
dichroic_ratio = corrected_vertical_absorbance_data.div(corrected_horizontal_absorbance_data.values, axis=0)
baseline_dichroic_ratio = normalized_baseline_vertical_absorbance_data.div(normalized_baseline_horizontal_absorbance_data.values, axis=0)


###### Plotting ########

formula = r"$A_{\text{corrected}} =1 - \frac{1-A_{\text{raw}}}{1-A_{\text{baseline}}}$"



fig, axs = plt.subplots(3, 1, figsize=(10, 18))
fig.suptitle(f'Polarized UV-vis for Batch {4}, prestrain {0}%, Sample {s_num} ({date})\n', fontsize=16, fontweight='bold')

colors = cm.Spectral([i / (vertical_absorbance_data.shape[1] - 1) for i in range(vertical_absorbance_data.shape[1])])

# Plot vertical data
for i, column in enumerate(normalized_vertical_transmittance_data.columns):
    axs[0].plot(wavelength, 1-normalized_vertical_transmittance_data[column], linestyle=':', label=f'Uncorrected Strain {column}', color=colors[i])
    axs[0].plot(wavelength, 1-corrected_vertical_transmittance_data[column], label=f'Corrected Strain {column}', color=colors[i])

axs[0].plot(wavelength, 1-normalized_baseline_vertical_transmittance_data, label='||-Baseline', color='black', linewidth=2)
axs[0].set_title('Corrected and Uncorrected Absorbance vs. Wavelength for ||-polarized light')
axs[0].set_xlabel('Wavelength (nm)')
axs[0].set_ylabel('Absorbance')
axs[0].set_xlim((400, 700))
axs[0].set_ylim((0, 1))
axs[0].legend(title='Strain', bbox_to_anchor=(1.05, 1), loc='upper left')
axs[0].text(0.75, 0.9, formula, fontsize=16, ha='center', va='center', transform=axs[0].transAxes)

# Plot horizontal data
for i, column in enumerate(normalized_horizontal_transmittance_data.columns):
    axs[1].plot(wavelength, 1-normalized_horizontal_transmittance_data[column], linestyle=':', label=f'Uncorrected Strain {column}', color=colors[i])
    axs[1].plot(wavelength, 1-corrected_horizontal_transmittance_data[column], label=f'Corrected Strain {column}', color=colors[i])

axs[1].plot(wavelength, 1-normalized_baseline_horizontal_transmittance_data, label='⊥-Baseline', color='black', linewidth=2)
axs[1].set_title('Corrected and Uncorrected Absorbance vs. Wavelength for ⊥-polarized light')
axs[1].set_xlabel('Wavelength (nm)')
axs[1].set_ylabel('Absorbance')
axs[1].set_xlim((400, 700))
axs[1].set_ylim((0, 1))
axs[1].legend(title='Strain', bbox_to_anchor=(1.05, 1), loc='upper left')

# Plot dichroic ratio
for i, column in enumerate(dichroic_ratio.columns):
    axs[2].plot(wavelength, dichroic_ratio[column], label=f'{column}', color=colors[i])
axs[2].plot(wavelength, baseline_dichroic_ratio, label='Baseline', color='black', linewidth=2, linestyle='--')

axs[2].set_title(r'Dichroic Ratio ($A_{\parallel}/A_{\perp}$) vs. Wavelength')
axs[2].set_xlabel('Wavelength (nm)')
axs[2].set_ylabel('Dichroic Ratio')
axs[2].set_xlim((400, 700))
axs[2].set_ylim((0.9, 1.3))

axs[2].legend(title='Strain', bbox_to_anchor=(1.05, 1), loc='upper left')

plt.tight_layout()
plt.show()
