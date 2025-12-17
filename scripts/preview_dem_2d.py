import rasterio
import matplotlib.pyplot as plt

dem_path = "data/turkey_dem_90m.tif"

with rasterio.open(dem_path) as dataset:
    elevation = dataset.read(1)

plt.imshow(elevation, cmap="terrain")
plt.colorbar(label="Elevation (meters)")
plt.title("Turkey DEM – 2D Preview")
plt.show()
