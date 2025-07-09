import json
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

def process_osm_data(geojson_path, osm_json_paths, output_geojson_path):
    # Load the merged census and geo data
    census_geo_df = gpd.read_file(geojson_path)

    # Ensure the CRS is set for spatial operations
    # TIGER/Line Shapefiles often use EPSG:4269 (NAD83)
    if census_geo_df.crs is None:
        census_geo_df = census_geo_df.set_crs("EPSG:4269", allow_override=True)
    elif census_geo_df.crs.to_epsg() != 4269:
        print(f"Reprojecting census_geo_df from {census_geo_df.crs} to EPSG:4269")
        census_geo_df = census_geo_df.to_crs(epsg=4269)

    for osm_json_path in osm_json_paths:
        amenity_name = osm_json_path.split("la_")[1].split(".json")[0] # Extract amenity name (e.g., parks, restaurants)
        print(f"Processing {amenity_name} from {osm_json_path}...")

        with open(osm_json_path, "r") as f:
            osm_data = json.load(f)

        elements = osm_data.get("elements", [])
        
        # Create a list of shapely Point objects from OSM elements
        # Filter out elements that are not nodes or do not have lat/lon
        points = []
        for elem in elements:
            if elem.get("type") == "node" and "lat" in elem and "lon" in elem:
                points.append(Point(elem["lon"], elem["lat"]))
        
        if not points:
            print(f"No valid points found for {amenity_name}. Skipping spatial join.")
            census_geo_df[f"num_{amenity_name}"] = 0 # Add column with zero if no points
            continue

        # Create a GeoDataFrame from the points, setting initial CRS to WGS84 (EPSG:4326)
        amenities_gdf = gpd.GeoDataFrame(geometry=points, crs="EPSG:4326")

        # Reproject amenities_gdf to match the CRS of census_geo_df before spatial join
        if amenities_gdf.crs != census_geo_df.crs:
            print(f"Reprojecting amenities_gdf from {amenities_gdf.crs} to {census_geo_df.crs}")
            amenities_gdf = amenities_gdf.to_crs(census_geo_df.crs)

        # Perform a spatial join to count amenities within each census tract
        # sjoin with \'within\' predicate means amenities_gdf points are within census_geo_df polygons
        joined_gdf = gpd.sjoin(amenities_gdf, census_geo_df, how="inner", predicate="within")

        # Count amenities per census tract (based on the index of the census_geo_df)
        amenity_counts = joined_gdf.groupby(joined_gdf.index_right).size().rename(f"num_{amenity_name}")

        # Add the counts back to the original census_geo_df
        census_geo_df = census_geo_df.merge(amenity_counts, left_index=True, right_index=True, how="left")
        
        # Fill NaN values (tracts with no amenities) with 0
        census_geo_df[f"num_{amenity_name}"] = census_geo_df[f"num_{amenity_name}"].fillna(0).astype(int)

    # Save the updated GeoJSON file
    census_geo_df.to_file(output_geojson_path, driver='GeoJSON')
    print(f"Updated GeoJSON with amenity counts saved to {output_geojson_path}")

if __name__ == "__main__":
    census_geojson = "california_census_tracts_population.geojson"
    osm_jsons = ["la_parks.json", "la_restaurants.json"]
    output_final_geojson = "california_census_tracts_enriched.geojson"

    print("Starting OSM data processing and integration...")
    process_osm_data(census_geojson, osm_jsons, output_final_geojson)


