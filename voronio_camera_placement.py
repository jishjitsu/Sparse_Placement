import numpy as np
from scipy.spatial import Voronoi
from shapely.geometry import Polygon, Point
from shapely.ops import unary_union


def generate_initial_points(min_lat, max_lat, min_lon, max_lon, num_points):
    lats = np.random.uniform(min_lat, max_lat, num_points)
    lons = np.random.uniform(min_lon, max_lon, num_points)
    return np.column_stack((lons, lats))


def place_cameras_voronoi(points, camera_range, num_cameras):
    # Get bounding box
    min_lat = min(points, key=lambda x: x[0])[0]
    max_lat = max(points, key=lambda x: x[0])[0]
    min_lon = min(points, key=lambda x: x[1])[1]
    max_lon = max(points, key=lambda x: x[1])[1]

    # Generate initial points
    initial_points = generate_initial_points(min_lat, max_lat, min_lon, max_lon, num_cameras)

    # Create Voronoi diagram
    vor = Voronoi(initial_points)

    # Place cameras at Voronoi cell centroids
    cameras = []
    for region_index in vor.point_region:
        vertices = vor.regions[region_index]
        if not -1 in vertices:  # Ensure region is bounded
            polygon = Polygon([vor.vertices[i] for i in vertices])
            if polygon.is_valid:
                centroid = polygon.centroid
                cameras.append((centroid.y, centroid.x))

    return cameras