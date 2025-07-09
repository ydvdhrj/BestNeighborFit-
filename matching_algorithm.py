import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from scipy.spatial.distance import euclidean
import joblib # To save and load the scaler
import os # Import the os module

def load_and_prepare_data(csv_path):
    df = pd.read_csv(csv_path)
    geoids = df["GEOID"]
    features_df = df.drop(columns=["GEOID"])

    # Load the scaler if it exists, otherwise create and fit a new one
    scaler_path = "scaler.joblib"
    if os.path.exists(scaler_path):
        scaler = joblib.load(scaler_path)
    else:
        scaler = MinMaxScaler()
        scaler.fit(features_df) # Fit the scaler on the original (unscaled) features
        joblib.dump(scaler, scaler_path) # Save the scaler

    scaled_features = scaler.transform(features_df)
    scaled_df = pd.DataFrame(scaled_features, columns=features_df.columns, index=features_df.index)
    scaled_df["GEOID"] = geoids
    return scaled_df, scaler, features_df.columns.tolist()

def get_recommendations(user_preferences_original_scale, scaled_neighborhood_data, feature_columns, scaler, k=5):
    # Create a DataFrame for user preferences from original scale
    user_df_original_scale = pd.DataFrame([user_preferences_original_scale])
    
    # Ensure user_df_original_scale has all feature columns, fill missing with 0 or a sensible default
    for col in feature_columns:
        if col not in user_df_original_scale.columns:
            user_df_original_scale[col] = 0 
    user_df_original_scale = user_df_original_scale[feature_columns] 

    # Scale user preferences using the same scaler fitted on the neighborhood data
    scaled_user_preferences = scaler.transform(user_df_original_scale)
    scaled_user_vector = scaled_user_preferences[0] 

    # Calculate Euclidean distance between user preferences and each neighborhood
    distances = []
    for index, row in scaled_neighborhood_data.iterrows():
        neighborhood_vector = row[feature_columns].values 
        dist = euclidean(scaled_user_vector, neighborhood_vector)
        distances.append((row["GEOID"], dist))

    # Sort by distance and get top K
    distances.sort(key=lambda x: x[1])
    top_k_recommendations = distances[:k]
