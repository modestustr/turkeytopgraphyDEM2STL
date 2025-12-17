"""
This script demonstrates how to download DEM data from OpenTopography
using their official API.

IMPORTANT:
- You MUST create a free OpenTopography account
- You MUST generate an API key
- You MUST insert your own API key below

Without a valid API key, this script WILL NOT work.
"""

import os
import requests

# -------------------------------------------------
# USER CONFIGURATION (REQUIRED)
# -------------------------------------------------

# 1. Create an account at https://opentopography.org
# 2. Generate an API key from your user profile
# 3. Paste the key here

OPENTOPO_API_KEY = "PUT_YOUR_API_KEY_HERE"

# -------------------------------------------------
# DATA REQUEST PARAMETERS
# -------------------------------------------------

# OpenTopography Global DEM API endpoint
BASE_URL = "https://portal.opentopography.org/API/globaldem"

# Dataset examples:
# - SRTMGL1 (30m)
# - SRTMGL3 (90m)
# - COP90 (Copernicus 90m)
DATASET = "COP90"

# Bounding box for Turkey (approximate)
# west, south, east, north
BBOX = {
    "west": 26.0,
    "south": 36.0,
    "east": 45.0,
    "north": 42.0
}

OUTPUT_DIR = "data"
OUTPUT_FILE = "turkey_dem_90m.tif"
OUTPUT_PATH = os.path.join(OUTPUT_DIR, OUTPUT_FILE)

# -------------------------------------------------
# DOWNLOAD FUNCTION
# -------------------------------------------------

def download_dem():
    if OPENTOPO_API_KEY == "PUT_YOUR_API_KEY_HERE":
        raise RuntimeError("Please insert your OpenTopography API key.")

    params = {
        "demtype": DATASET,
        "west": BBOX["west"],
        "south": BBOX["south"],
        "east": BBOX["east"],
        "north": BBOX["north"],
        "outputFormat": "GTiff",
        "API_Key": OPENTOPO_API_KEY
    }

    print("Requesting DEM from OpenTopography...")
    print("Dataset:", DATASET)
    print("Bounding box:", BBOX)

    response = requests.get(BASE_URL, params=params, stream=True)
    response.raise_for_status()

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with open(OUTPUT_PATH, "wb") as file:
        for chunk in response.iter_content(chunk_size=1024 * 1024):
            if chunk:
                file.write(chunk)

    print("Download completed successfully.")
    print("Saved to:", OUTPUT_PATH)

# -------------------------------------------------
# ENTRY POINT
# -------------------------------------------------

if __name__ == "__main__":
    download_dem()
