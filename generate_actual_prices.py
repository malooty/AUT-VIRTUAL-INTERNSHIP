import pandas as pd
import numpy as np

# Load the CSV file
file_path = 'team_name1_price_fcst.csv'
df = pd.read_csv(file_path)

# Convert the date column to string
df['date'] = df['date'].astype(str)

# Generate synthetic actual prices by adding random noise to the forecasted prices
np.random.seed(42)  # For reproducibility
noise = np.random.normal(0, 2, size=len(df))  # Adjust mean and standard deviation as needed
df['actual_price'] = df['price_fcst'] + noise

# Save the updated CSV file
df.to_csv('team_name1_price_fcst_with_actual.csv', index=False)

print("Generated actual prices and saved to 'data/team_name1_price_fcst_with_actual.csv'")
