import numpy as np

def place_cameras_hex(points, camera_range):
    # Get the bounding box of the area
    min_lat = min(points, key=lambda x: x[0])[0]
    max_lat = max(points, key=lambda x: x[0])[0]
    min_lon = min(points, key=lambda x: x[1])[1]
    max_lon = max(points, key=lambda x: x[1])[1]

    lat_range = camera_range / 111320
    lon_range = camera_range / (40075000 * np.cos(np.deg2rad((min_lat + max_lat) / 2)) / 360)
    lat_step = lat_range * 3/2
    lon_step = lon_range * np.sqrt(3)

    cameras = []

    lat = min_lat
    row = 0
    while lat <= max_lat:
        lon = min_lon + (row % 2) * (lon_step / 2)
        while lon <= max_lon:
            cameras.append((lat, lon))
            lon += lon_step
        lat += lat_step
        row += 1

    return cameras