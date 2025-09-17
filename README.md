# Map Services

A Python package providing Swiss Topo elevation services and map utilities.

## Overview

This package exposes functionality for accessing Swiss topographic elevation data, originally from the [pyriadne repository](https://github.com/supsi-dacd-isaac/pyriadne/blob/main/utils/swisstopo_elevation.py).

## Installation

```bash
pip install -e .
```

For development:
```bash
pip install -e ".[dev]"
```

## Usage

### Basic Usage

```python
from map_services.swisstopo_elevation import get_elevation, get_elevation_batch

# Get elevation for a single point (Zurich coordinates)
elevation = get_elevation(8.5417, 47.3769)
print(f"Elevation: {elevation} meters")

# Get elevation for multiple points
coordinates = [
    (8.5417, 47.3769),  # Zurich
    (7.4474, 46.9480),  # Bern
]
elevations = get_elevation_batch(coordinates)
print(f"Elevations: {elevations}")
```

### Using the Client Class

```python
from map_services.swisstopo_elevation import SwissTopoElevationClient

# Create a client instance
client = SwissTopoElevationClient()

# Get elevation for a single point
elevation = client.get_elevation(8.5417, 47.3769)
print(f"Elevation: {elevation} meters")

# Get elevation for multiple points
coordinates = [(8.5417, 47.3769), (7.4474, 46.9480)]
elevations = client.get_elevation_batch(coordinates)
print(f"Elevations: {elevations}")
```

## Development

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
black map_services tests
```

### Linting

```bash
flake8 map_services tests
```

## API Reference

### Functions

- `get_elevation(longitude, latitude)`: Get elevation for a single coordinate point
- `get_elevation_batch(coordinates)`: Get elevation for multiple coordinate points

### Classes

- `SwissTopoElevationClient`: Main client class for accessing elevation services

## License

MIT License - see LICENSE file for details.

## Note

This package contains template/placeholder code. The actual implementation should be copied from the [pyriadne repository](https://github.com/supsi-dacd-isaac/pyriadne/blob/main/utils/swisstopo_elevation.py) to provide full functionality.
