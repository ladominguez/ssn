from geopy.distance import great_circle
import numpy as np

def interpolate_great_circle(coord1, coord2, num_points=10):
    """
    Interpolates points along a great-circle path between two geographical coordinates.
    
    Parameters:
        coord1 (tuple): (latitude, longitude) of the starting point.
        coord2 (tuple): (latitude, longitude) of the ending point.
        num_points (int): Number of interpolated points (including start and end).
        
    Returns:
        list of tuples: Interpolated points as (latitude, longitude).
    """
    lat1, lon1 = np.radians(coord1)
    lat2, lon2 = np.radians(coord2)
    
    interpolated_points = []
    
    for fraction in np.linspace(0, 1, num_points):
        delta_sigma = np.arccos(
            np.sin(lat1) * np.sin(lat2) + np.cos(lat1) * np.cos(lat2) * np.cos(lon2 - lon1)
        )
        
        a = np.sin((1 - fraction) * delta_sigma) / np.sin(delta_sigma)
        b = np.sin(fraction * delta_sigma) / np.sin(delta_sigma)
        
        x = a * np.cos(lat1) * np.cos(lon1) + b * np.cos(lat2) * np.cos(lon2)
        y = a * np.cos(lat1) * np.sin(lon1) + b * np.cos(lat2) * np.sin(lon2)
        z = a * np.sin(lat1) + b * np.sin(lat2)
        
        lat = np.degrees(np.arctan2(z, np.sqrt(x**2 + y**2)))
        lon = np.degrees(np.arctan2(y, x))
        
        interpolated_points.append((lat, lon))
    interpolated_points = np.array(interpolated_points)
    
    return interpolated_points

# Example usage:
#start = (37.7749, -122.4194)  # San Francisco, CA
#end = (40.7128, -74.0060)  # New York, NY
#interpolated_coords = interpolate_great_circle(start, end, num_points=10)

