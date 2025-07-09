import pandas as pd
import geopandas as gpd
import requests
import zipfile
import os

def download_census_data(api_key, year='2022', dataset='acs5', variables='B01001_001E', state_fips='06', output_csv='california_population_tracts.csv'):
    print(f"Downloading Census data for {year}...")
    base_url = f"https://api.census.gov/data/{year}/acs/{dataset}?get={variables}&for=tract:*&in=state:{state_fips}&key={api_key}" # Corrected API endpoint <mcreference link="https://www.census.gov/data/developers/data-sets/acs-5year/2022.html" index="2"></mcreference>
    import certifi
    response = requests.get(base_url, verify=certifi.where())
    response.raise_for_status() # Raise an exception for HTTP errors
    data = response.json()

    # The first row is the header
    df = pd.DataFrame(data[1:], columns=data[0])
    df.rename(columns={'B01001_001E': 'total_population', 'tract': 'TRACTCE', 'state': 'STATEFP', 'county': 'COUNTYFP'}, inplace=True)
    df['GEOID'] = df['STATEFP'] + df['COUNTYFP'] + df['TRACTCE']
    df.to_csv(output_csv, index=False)
    print(f"Census data saved to {output_csv}")
    return output_csv

def download_tiger_shapefile(year='2022', state_fips='06', output_shp_zip='tl_2022_06_tract.zip', output_shp_dir='tl_2022_06_tract'):
    print(f"Downloading TIGER/Line Shapefiles for {year}...")
    url = f"https://www2.census.gov/geo/tiger/TIGER{year}/TRACT/tl_{year}_{state_fips}_tract.zip"
    import certifi
    response = requests.get(url, stream=True, verify=certifi.where()) # Temporarily disable SSL verification to debug SSLError
    response.raise_for_status()

    with open(output_shp_zip, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f"Shapefile zip downloaded to {output_shp_zip}")

    with zipfile.ZipFile(output_shp_zip, 'r') as zip_ref:
        zip_ref.extractall(output_shp_dir)
    print(f"Shapefile extracted to {output_shp_dir}")
    return os.path.join(output_shp_dir, f'tl_{year}_{state_fips}_tract.shp')

def merge_data_to_geojson(census_csv, shp_path, output_geojson='california_census_tracts_population.geojson'):
    print("Merging Census data with Shapefile...")
    census_df = pd.read_csv(census_csv, dtype={'GEOID': str, 'STATEFP': str, 'COUNTYFP': str, 'TRACTCE': str})
    geo_df = gpd.read_file(shp_path)

    # Ensure GEOID is consistent for merging
    geo_df['GEOID'] = geo_df['GEOID'].astype(str)

    # Perform the merge
    merged_gdf = geo_df.merge(census_df, on='GEOID', how='left')

    # Handle potential CRS issues if not already set
    if merged_gdf.crs is None:
        merged_gdf = merged_gdf.set_crs("EPSG:4269", allow_override=True) # NAD83

    merged_gdf.to_file(output_geojson, driver='GeoJSON')
    print(f"Merged GeoJSON saved to {output_geojson}")
    return output_geojson

if __name__ == "__main__":
    # IMPORTANT: Replace 'YOUR_CENSUS_API_KEY' with your actual Census API key
    # You can obtain one for free from: https://www.census.gov/data/developers/guidance/api-user-guide.html
    CENSUS_API_KEY = os.getenv("CENSUS_API_KEY", "YOUR_CENSUS_API_KEY")

    if CENSUS_API_KEY == "YOUR_CENSUS_API_KEY":
        print("WARNING: CENSUS_API_KEY is not set. Please set it as an environment variable or replace 'YOUR_CENSUS_API_KEY' in the script.")
        print("Proceeding with dummy key, but data download will likely fail.")

    # Define paths and parameters
    CENSUS_CSV_PATH = 'california_population_tracts.csv'
    TIGER_SHP_ZIP = 'tl_2022_06_tract.zip'
    TIGER_SHP_DIR = 'tl_2022_06_tract'
    OUTPUT_GEOJSON_PATH = 'california_census_tracts_population.geojson'

    # Clean up previous downloads if they exist
    if os.path.exists(CENSUS_CSV_PATH):
        os.remove(CENSUS_CSV_PATH)
    if os.path.exists(TIGER_SHP_ZIP):
        os.remove(TIGER_SHP_ZIP)
    if os.path.exists(TIGER_SHP_DIR):
        import shutil
        shutil.rmtree(TIGER_SHP_DIR)

    # Step 1: Download Census Data
    census_csv = download_census_data(CENSUS_API_KEY, output_csv=CENSUS_CSV_PATH)

    # Step 2: Download TIGER/Line Shapefile
    shp_path = download_tiger_shapefile(output_shp_zip=TIGER_SHP_ZIP, output_shp_dir=TIGER_SHP_DIR)

    # Step 3: Merge and save as GeoJSON
    merge_data_to_geojson(census_csv, shp_path, output_geojson=OUTPUT_GEOJSON_PATH)

    print("Data preparation for california_census_tracts_population.geojson complete.")

    # Clean up downloaded zip and extracted shapefile directory
    if os.path.exists(TIGER_SHP_ZIP):
        os.remove(TIGER_SHP_ZIP)
    if os.path.exists(TIGER_SHP_DIR):
        import shutil
        shutil.rmtree(TIGER_SHP_DIR)

    print("Temporary files cleaned up.")