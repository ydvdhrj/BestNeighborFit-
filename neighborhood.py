from flask import Blueprint, jsonify, request
import pandas as pd
import joblib
import os
from scipy.spatial.distance import euclidean

neighborhood_bp = Blueprint('neighborhood', __name__)


# Load the processed data and scaler from the project directory
DATA_PATH = os.path.join(os.path.dirname(__file__), 'california_census_tracts_features.csv')
SCALER_PATH = os.path.join(os.path.dirname(__file__), 'scaler.joblib')

# Global variables to store data and scaler
neighborhood_data = None
scaler = None
feature_columns = None

def load_data():
    global neighborhood_data, scaler, feature_columns
    if neighborhood_data is None:
        # Load the processed neighborhood data
        df = pd.read_csv(DATA_PATH)
        geoids = df["GEOID"]
        features_df = df.drop(columns=["GEOID"])
        
        # Load the scaler
        scaler = joblib.load(SCALER_PATH)
        
        # Scale the features
        scaled_features = scaler.transform(features_df)
        scaled_df = pd.DataFrame(scaled_features, columns=features_df.columns, index=features_df.index)
        scaled_df["GEOID"] = geoids
        
        neighborhood_data = scaled_df
        feature_columns = features_df.columns.tolist()

@neighborhood_bp.route('/neighborhoods/recommend', methods=['POST'])
def get_recommendations():
    load_data()  # Ensure data is loaded
    
    try:
        # Get user preferences from request
        user_preferences = request.json
        k = user_preferences.get('k', 5)  # Number of recommendations, default to 5
        
        # Extract the preference values
        preferences = {
            'population_density': user_preferences.get('population_density', 0),
            'parks_per_sqkm': user_preferences.get('parks_per_sqkm', 0),
            'restaurants_per_sqkm': user_preferences.get('restaurants_per_sqkm', 0)
        }
        
        # Create a DataFrame for user preferences
        user_df = pd.DataFrame([preferences])
        
        # Ensure all feature columns are present
        for col in feature_columns:
            if col not in user_df.columns:
                user_df[col] = 0
        user_df = user_df[feature_columns]
        
        # Scale user preferences
        scaled_user_preferences = scaler.transform(user_df)
        scaled_user_vector = scaled_user_preferences[0]
        
        # Calculate distances
        distances = []
        for index, row in neighborhood_data.iterrows():
            neighborhood_vector = row[feature_columns].values
            dist = euclidean(scaled_user_vector, neighborhood_vector)
            distances.append({
                'geoid': row["GEOID"],
                'distance': dist
            })
        
        # Sort by distance and get top k
        distances.sort(key=lambda x: x['distance'])
        top_recommendations = distances[:k]
        
        return jsonify({
            'status': 'success',
            'user_preferences': preferences,
            'recommendations': top_recommendations
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400

@neighborhood_bp.route('/neighborhoods/features', methods=['GET'])
def get_feature_info():
    load_data()  # Ensure data is loaded
    
    # Load original data to get feature ranges
    original_df = pd.read_csv(DATA_PATH)
    
    feature_info = {}
    for col in feature_columns:
        feature_info[col] = {
            'min': float(original_df[col].min()),
            'max': float(original_df[col].max()),
            'mean': float(original_df[col].mean()),
            'description': get_feature_description(col)
        }
    
    return jsonify({
        'status': 'success',
        'features': feature_info
    })

def get_feature_description(feature_name):
    descriptions = {
        'population_density': 'Population per square kilometer',
        'parks_per_sqkm': 'Number of parks per square kilometer',
        'restaurants_per_sqkm': 'Number of restaurants per square kilometer'
    }
    return descriptions.get(feature_name, 'No description available')

@neighborhood_bp.route('/neighborhoods/<geoid>', methods=['GET'])
def get_neighborhood_details(geoid):
    load_data()  # Ensure data is loaded
    
    # Find the neighborhood by GEOID
    neighborhood = neighborhood_data[neighborhood_data['GEOID'] == float(geoid)]
    
    if neighborhood.empty:
        return jsonify({
            'status': 'error',
            'message': 'Neighborhood not found'
        }), 404
    
    # Get the original (unscaled) values
    original_df = pd.read_csv(DATA_PATH)
    original_neighborhood = original_df[original_df['GEOID'] == float(geoid)]
    
    if original_neighborhood.empty:
        return jsonify({
            'status': 'error',
            'message': 'Neighborhood data not found'
        }), 404
    
    neighborhood_info = {
        'geoid': geoid,
        'features': {}
    }
    
    for col in feature_columns:
        neighborhood_info['features'][col] = {
            'value': float(original_neighborhood[col].iloc[0]),
            'description': get_feature_description(col)
        }
    
    return jsonify({
        'status': 'success',
        'neighborhood': neighborhood_info
    })