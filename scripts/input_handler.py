def get_user_input():
    points = []
    for i in range(4):
        lat = float(input(f"Enter latitude for point {i+1}: "))
        lon = float(input(f"Enter longitude for point {i+1}: "))
        points.append((lat, lon))
    camera_range = float(input("Enter camera range in meters: "))
    return points, camera_range
