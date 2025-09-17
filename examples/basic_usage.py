#!/usr/bin/env python3
"""
Basic usage example for the map_services package.

This example demonstrates how to use the Swiss Topo elevation services.
"""

from map_services.swisstopo_elevation import SwissTopoElevationClient, get_elevation, get_elevation_batch


def main():
    """Demonstrate basic usage of the elevation services."""
    
    print("=== Map Services - Swiss Topo Elevation Example ===\n")
    
    # Example 1: Using convenience functions
    print("1. Using convenience functions:")
    
    # Swiss coordinates (Zurich)
    zurich_lon, zurich_lat = 8.5417, 47.3769
    print(f"Getting elevation for Zurich ({zurich_lon}, {zurich_lat})")
    
    # Note: This will fail in the current template implementation
    # as we don't have access to the real Swiss Topo API
    try:
        elevation = get_elevation(zurich_lon, zurich_lat)
        print(f"Elevation: {elevation} meters")
    except Exception as e:
        print(f"API call failed (expected with template): {e}")
    
    print()
    
    # Example 2: Using the client class
    print("2. Using the client class:")
    
    client = SwissTopoElevationClient()
    print(f"Client initialized with base URL: {client.base_url}")
    
    # Example coordinates for several Swiss cities
    coordinates = [
        (8.5417, 47.3769),  # Zurich
        (7.4474, 46.9480),  # Bern
        (6.1432, 46.2044),  # Geneva
    ]
    
    city_names = ["Zurich", "Bern", "Geneva"]
    
    print("\nBatch elevation lookup:")
    try:
        elevations = client.get_elevation_batch(coordinates)
        for name, (lon, lat), elev in zip(city_names, coordinates, elevations):
            print(f"  {name} ({lon}, {lat}): {elev} meters")
    except Exception as e:
        print(f"Batch API call failed (expected with template): {e}")
    
    print("\n=== Example completed ===")
    print("\nNote: This is a template implementation.")
    print("Replace the swisstopo_elevation.py content with the actual")
    print("implementation from https://github.com/supsi-dacd-isaac/pyriadne")


if __name__ == "__main__":
    main()