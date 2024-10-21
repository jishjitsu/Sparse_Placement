from scripts.input_handler import get_user_input
from scripts.area_calculator import calculate_area
from scripts.camera_placement import place_cameras
from scripts.hexagonal_camera_placement import place_cameras_hex
from scripts.greedy_camera_placement import place_cameras_greedy
from scripts.k_means_camera_placement import place_cameras_kmeans
from scripts.voronio_camera_placement import place_cameras_voronoi
from scripts.ILP_camera_placement import place_cameras_ilp
from scripts.map_visualization import visualize_map

def main():
    print("Taking user input...")
    points, camera_range = get_user_input()
    print("Input taken successfully")
    
    area = calculate_area(points)
    print(f"Calculated area: {area} square meters")

    cameras1 = place_cameras(points, camera_range)
    cameras2 = place_cameras_hex(points, camera_range)
    cameras3 = place_cameras_greedy(points, camera_range)

    print(f"Camera placements (algorithm 1): {cameras1}")
    print(f"Camera placements (hexagonal): {cameras2}")
    print(f"Camera placements (greedy): {cameras3}")

    map1 = visualize_map(points, cameras1, camera_range)
    map1.save('camera_placement_map.html')

    map2 = visualize_map(points, cameras2, camera_range)
    map2.save('hexagonal_placement_map.html')

    map3 = visualize_map(points, cameras3, camera_range)
    map3.save('greedy_placement_map.html')

    print("Map saved as 'camera_placement_map.html'")
    print("Map saved as 'hexagonal_placement_map.html'")
    print("Map saved as 'greedy_placement_map.html'")

if __name__ == "__main__":
    main()
