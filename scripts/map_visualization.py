import folium
import numpy as np


def visualize_map(points, cameras, camera_range):
    # Create a map centered around the average point
    center_lat = np.mean([point[0] for point in points])
    center_lon = np.mean([point[1] for point in points])
    m = folium.Map(location=[center_lat, center_lon], zoom_start=13)

    # Highlight area
    folium.Polygon(locations=points, color='blue', fill=True).add_to(m)

    # Place cameras with range circles
    for camera in cameras:
        folium.Marker(location=camera, icon=folium.Icon(color='red')).add_to(m)
        folium.Circle(
            radius=camera_range,
            location=camera,
            color='red',
            fill=True,
            fill_color='red'
        ).add_to(m)

    return m

