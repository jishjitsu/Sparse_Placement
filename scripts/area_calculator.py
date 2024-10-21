import numpy as np

def calculate_area(points):
    x = np.array([point[1] for point in points])
    y = np.array([point[0] for point in points])
    return 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))
