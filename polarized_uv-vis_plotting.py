import pandas as pd

# Load the CSV file into a pandas DataFrame
file_path = '/Users/adrian/Documents/UV-vis/Carlos_P3HT_9-8-24/Batch 5 Samples - Sample 6 Raw Data.csv'
df = pd.read_csv(file_path)

# Display the first few rows of the DataFrame to understand its structure
print(df.head())
