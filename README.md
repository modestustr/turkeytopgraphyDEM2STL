# Pure Python DEM to 3D STL — no GIS required

This repository demonstrates how to generate a 3D topographic STL model
of Turkey using real elevation data, pure Python, and no GIS software.

The project focuses on understanding the full pipeline rather than
producing a polished or 3D-print-ready model.

------------------------------------------------------------------------

## Project Goals

-   Use real-world elevation data
-   Avoid GIS software (QGIS, ArcGIS)
-   Work entirely in Python
-   Scale terrain to A5 size (210 × 148 mm)
-   Export a true 3D STL mesh

------------------------------------------------------------------------

## Repository Structure

    turkey-topography-python/
    ├── scripts/
    │   ├── download_dem_opentopography.py
    │   ├── preview_dem_2d.py
    │   └── dem_to_stl_a5.py
    ├── data/
    ├── outputs/
    ├── .gitignore
    └── README.md

------------------------------------------------------------------------

# Quick Start

1. Place DEM in data/
2. Run download script (with API key)
3. Preview with preview_dem_2d.py
4. Generate STL with dem_to_stl_a5.py

## Data Source

Elevation data is provided by **OpenTopography**.

OpenTopography requires an API key to download DEM data
programmatically.

------------------------------------------------------------------------

## OpenTopography API Key

1.  Create a free account at https://opentopography.org
2.  Generate an API key from your user profile
3.  Insert the key into the download script

Example:

``` python
API_KEY = "PUT_YOUR_API_KEY_HERE"
```

API keys must **not** be committed to GitHub.

------------------------------------------------------------------------

## Download DEM Data

``` bash
python scripts/download_dem_opentopography.py
```

This script downloads a GeoTIFF DEM covering Turkey and saves it
locally.

------------------------------------------------------------------------

## Preview DEM (Optional)

``` bash
python scripts/preview_dem_2d.py
```

Displays a simple 2D elevation preview to verify data integrity.

------------------------------------------------------------------------

## Generate STL

``` bash
python scripts/dem_to_stl_a5.py
```

This step is slow and memory-intensive.

------------------------------------------------------------------------

## Output

    outputs/turkey_topography_A5.stl

Large STL files may exceed hundreds of megabytes.

------------------------------------------------------------------------

## Notes

This project is exploratory.

The goal is to verify that a real 3D terrain model can be generated
using only Python and open elevation data.

------------------------------------------------------------------------

## License

MIT License
