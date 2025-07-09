import geopandas as gpd
import pandas as pd

def prepare_data_for_algorithm(input_geojson_path, output_csv_path):
    print(f"Loading data from {input_geojson_path}...")
    gdf = gpd.read_file(input_geojson_path)

    # Extract numerical features. Assuming 'GEOID' and amenity counts are the features.
    # Adjust this list based on the actual features needed for the matching algorithm.
    # Based on Problem Analysis & User Research.md, features include population density, parks, restaurants.
    # The 'GEOID' is likely an identifier.
    # We need to ensure the columns match what the scaler expects.
    
    # Identify columns that are numerical and relevant for the algorithm
    # Exclude 'geometry' and any other non-feature columns
    feature_columns = [col for col in gdf.columns if col not in ['geometry', 'GEOID', 'NAME', 'STATEFP', 'COUNTYFP', 'TRACTCE', 'AFFGEOID', 'LSAD', 'ALAND', 'AWATER']]
    
    # Ensure 'GEOID' is included as it's used as an identifier in matching_algorithm.py
    # and generate_scaler.py drops it before scaling.
    df_features = gdf[['GEOID'] + feature_columns].copy()

    print(f"Saving features to {output_csv_path}...")
    df_features.to_csv(output_csv_path, index=False)
    print("Data preparation complete.")

if __name__ == "__main__":
    input_geojson = "california_census_tracts_enriched.geojson"
    output_csv = "california_census_tracts_features.csv"
    prepare_data_for_algorithm(input_geojson, output_csv)