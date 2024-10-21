import numpy as np
from shapely.geometry import Point, Polygon
from shapely.ops import unary_union


def place_cameras_greedy(points, camera_range):
    area = Polygon(points)

    lat_range = camera_range / 111320
    lon_range = camera_range / (40075000 * np.cos(np.deg2rad(area.centroid.y)) / 360)
    cameras = []
    uncovered_area = area

    while not uncovered_area.is_empty:
        best_camera_position = None
        max_new_coverage = 0
        min_lat, min_lon, max_lat, max_lon = area.bounds
        lat = min_lat
        while lat <= max_lat:
            lon = min_lon
            while lon <= max_lon:
                candidate_camera = Point(lon, lat)
                coverage_area = candidate_camera.buffer(lat_range)
                new_coverage = coverage_area.intersection(uncovered_area).area

                if new_coverage > max_new_coverage:
                    max_new_coverage = new_coverage
                    best_camera_position = candidate_camera

                lon += lon_range
            lat += lat_range

        if best_camera_position:
            cameras.append((best_camera_position.y, best_camera_position.x))
            coverage_area = best_camera_position.buffer(lat_range)
            uncovered_area = uncovered_area.difference(coverage_area)

    return cameras