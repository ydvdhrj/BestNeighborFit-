import requests
import json
import os

# Bounding box for Los Angeles (approximate coordinates)
# [south, west, north, east]
LA_BOUNDING_BOX = "33.70, -118.67, 34.30, -118.15"

OVERPASS_URL = "http://overpass-api.de/api/interpreter"

def download_osm_data(amenity_type, amenity_value, output_filename, bbox):
    print(f"Downloading {amenity_type} data...")
    query = f"""
[out:json];
(node["{amenity_type}"="{amenity_value}"]({bbox});
  way["{amenity_type}"="{amenity_value}"]({bbox});
  relation["{amenity_type}"="{amenity_value}"]({bbox});
);
out center;
"""
    response = requests.post(OVERPASS_URL, data=query)
    response.raise_for_status() # Raise an exception for HTTP errors
    data = response.json()

    with open(output_filename, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Downloaded {amenity_type} data to {output_filename}")

if __name__ == "__main__":
    # Ensure the output directory exists if needed (not strictly necessary for root)
    # os.makedirs("data", exist_ok=True)

    # Download parks data
    download_osm_data(amenity_type="leisure", amenity_value="park", output_filename="la_parks.json", bbox=LA_BOUNDING_BOX)

    # Download restaurants data
    download_osm_data(amenity_type="amenity", amenity_value="restaurant", output_filename="la_restaurants.json", bbox=LA_BOUNDING_BOX)

    print("OSM data download complete.")