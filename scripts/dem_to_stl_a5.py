import numpy as np
import rasterio
from stl import mesh
from datetime import datetime

# -------------------------------------------------
# CONFIGURATION
# -------------------------------------------------

DEM_PATH = "data/turkey_dem_90m.tif"
OUTPUT_STL = "outputs/turkey_topography_A5.stl"

A5_WIDTH_MM = 210.0
A5_HEIGHT_MM = 148.0

MAX_HEIGHT_MM = 20.0
BASE_THICKNESS_MM = 3.0

DOWNSAMPLE_FACTOR = 8  # Increase if you run out of memory

# -------------------------------------------------
# LOGGING
# -------------------------------------------------

def log(message):
    now = datetime.now().strftime("%H:%M:%S")
    print(f"[{now}] {message}")

# -------------------------------------------------
# READ DEM (WINDOWED / DOWNSAMPLED)
# -------------------------------------------------

log("Started")
log("Opening DEM")

with rasterio.open(DEM_PATH) as dataset:
    total_rows, total_cols = dataset.height, dataset.width
    pixel_size_x, pixel_size_y = dataset.res

    rows = total_rows // DOWNSAMPLE_FACTOR
    cols = total_cols // DOWNSAMPLE_FACTOR

    log(f"Target grid size: {rows} x {cols}")

    elevation = dataset.read(
        1,
        out_shape=(rows, cols),
        resampling=rasterio.enums.Resampling.average
    )

log("DEM loaded")

# -------------------------------------------------
# CLEAN DATA
# -------------------------------------------------

elevation = np.nan_to_num(elevation)
elevation[elevation < 0] = 0

# -------------------------------------------------
# SCALE XY TO A5 SIZE
# -------------------------------------------------

log("Scaling XY dimensions")

width_meters = cols * pixel_size_x * DOWNSAMPLE_FACTOR
height_meters = rows * pixel_size_y * DOWNSAMPLE_FACTOR

scale_xy = min(
    A5_WIDTH_MM / width_meters,
    A5_HEIGHT_MM / height_meters
)

x_coords = np.arange(cols) * pixel_size_x * DOWNSAMPLE_FACTOR * scale_xy
y_coords = np.arange(rows) * pixel_size_y * DOWNSAMPLE_FACTOR * scale_xy

X, Y = np.meshgrid(x_coords, y_coords)

# -------------------------------------------------
# SCALE Z (HEIGHT)
# -------------------------------------------------

log("Scaling Z values")

z_scaled = elevation * (MAX_HEIGHT_MM / elevation.max())
z_scaled += BASE_THICKNESS_MM

# -------------------------------------------------
# CREATE STL MESH (TOP SURFACE)
# -------------------------------------------------

log("Creating mesh (this is slow)")
faces = []

for row in range(rows - 1):
    if row % 50 == 0:
        log(f"  processing row {row}/{rows}")

    for col in range(cols - 1):
        p1 = [X[row, col],     Y[row, col],     z_scaled[row, col]]
        p2 = [X[row + 1, col], Y[row + 1, col], z_scaled[row + 1, col]]
        p3 = [X[row, col + 1], Y[row, col + 1], z_scaled[row, col + 1]]
        p4 = [X[row + 1, col + 1], Y[row + 1, col + 1], z_scaled[row + 1, col + 1]]

        faces.append([p1, p2, p3])
        faces.append([p2, p4, p3])

log("Top surface created")

# -------------------------------------------------
# CREATE BASE (BOTTOM PLANE)
# -------------------------------------------------

log("Adding base")

base_z = 0.0

for row in range(rows - 1):
    for col in range(cols - 1):
        b1 = [X[row, col],     Y[row, col],     base_z]
        b2 = [X[row, col + 1], Y[row, col + 1], base_z]
        b3 = [X[row + 1, col], Y[row + 1, col], base_z]
        b4 = [X[row + 1, col + 1], Y[row + 1, col + 1], base_z]

        faces.append([b1, b2, b3])
        faces.append([b3, b2, b4])

log("Base added")

# -------------------------------------------------
# EXPORT STL
# -------------------------------------------------

log("Exporting STL")

terrain_mesh = mesh.Mesh(
    np.zeros(len(faces), dtype=mesh.Mesh.dtype)
)

for i, face in enumerate(faces):
    terrain_mesh.vectors[i] = face

terrain_mesh.save(OUTPUT_STL)

log("STL saved successfully")
