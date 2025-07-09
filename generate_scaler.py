import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import joblib

# Load the sample data
df = pd.read_csv('california_census_tracts_features.csv')
features_df = df.drop(columns=["GEOID"])

# Create and fit a new scaler
scaler = MinMaxScaler()
scaler.fit(features_df)  # Fit the scaler on the original (unscaled) features

# Save the scaler
joblib.dump(scaler, 'scaler.joblib')

print("Scaler has been generated and saved to scaler.joblib")