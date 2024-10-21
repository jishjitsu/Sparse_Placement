import numpy as np
from sklearn.cluster import KMeans

def place_cameras_kmeans(points, camera_range, num_cameras):

    points_array = np.array(points)

    # Apply K-Means clustering to find camera positions
    kmeans = KMeans(n_clusters=num_cameras)
    kmeans.fit(points_array)

    # Get the cluster centers (camera positions)
    camera_positions = kmeans.cluster_centers_

    # Convert camera positions to list of tuples
    cameras = [tuple(position) for position in camera_positions]

    return cameras
