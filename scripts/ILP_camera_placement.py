import numpy as np
from pulp import LpProblem, LpMinimize, LpVariable, lpSum, LpStatus, value

def place_cameras_ilp(points, camera_range):
    # Get bounding box
    min_lat = min(points, key=lambda x: x[0])[0]
    max_lat = max(points, key=lambda x: x[0])[0]
    min_lon = min(points, key=lambda x: x[1])[1]
    max_lon = max(points, key=lambda x: x[1])[1]

    # Convert camera range to degrees (approximate)
    lat_range = camera_range / 111320  # 1 degree latitude ~ 111.32 km
    lon_range = camera_range / (40075000 * np.cos(np.deg2rad((min_lat + max_lat) / 2)) / 360)  # 1 degree longitude varies

    # Define grid points
    lat_points = np.arange(min_lat, max_lat, lat_range)
    lon_points = np.arange(min_lon, max_lon, lon_range)
    grid_points = [(lat, lon) for lat in lat_points for lon in lon_points]

    # ILP problem definition
    problem = LpProblem("Camera_Placement", LpMinimize)

    # Decision variables
    camera_vars = LpVariable.dicts("Camera", grid_points, cat="Binary")

    # Objective function: minimize the number of cameras
    problem += lpSum([camera_vars[point] for point in grid_points])

    # Constraints: each original point must be covered by at least one camera
    for lat, lon in points:
        problem += lpSum([camera_vars[(g_lat, g_lon)] for g_lat, g_lon in grid_points
                          if np.sqrt((lat - g_lat)**2 + (lon - g_lon)**2) <= lat_range]) >= 1

    # Solve the problem
    problem.solve()

    # Extract camera positions
    cameras = [(lat, lon) for lat, lon in grid_points if value(camera_vars[(lat, lon)]) == 1]

    return cameras