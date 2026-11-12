import numpy as np
import pandas as pd
from scipy.signal import savgol_filter
import matplotlib.pyplot as plt

def calculate_displaced_kinematics(distances, fps):
    """
    Calculates velocity and acceleration from frame-to-frame distance steps.
    
    Parameters:
    - distances: List/Array of movement values between frames [d1_to_2, d2_to_3, ...]
    - fps: Frames per second of the video
    """
    distances = np.array(distances, dtype=float)
    total_intervals = len(distances)
    
    if total_intervals < 2:
        raise ValueError("Need at least 2 distance intervals to calculate acceleration.")
        
    dt = 1.0 / fps  # Time step per frame
    
    # 1. Smooth the raw displacement input to eliminate pixel tracking noise
    window_len = min(5, total_intervals if total_intervals % 2 != 0 else total_intervals - 1)
    if window_len >= 3:
        smoothed_distances = savgol_filter(distances, window_length=window_len, polyorder=1)
    else:
        smoothed_distances = distances

    # 2. Calculate Velocity (Units/Second)
    # Velocity = Distance step divided by time step
    velocities = smoothed_distances / dt
    
    # 3. Calculate Acceleration (Units/Second^2)
    # Acceleration = Change in velocity divided by time step
    dv = np.diff(velocities)
    accelerations = dv / dt
    
    # 4. Construct Timeline Matrix
    # Because 'distances' happen between frames, Timeline maps to interval endpoints
    timeline_data = {
        "Interval": np.arange(1, total_intervals + 1),
        "Time_Sec": np.arange(1, total_intervals + 1) * dt,
        "Raw_Distance": distances,
        "Speed": velocities,
        "Acceleration": np.insert(accelerations, 0, np.nan) # First interval has no prior speed change
    }
    
    #return pd.DataFrame(timeline_data)
    return accelerations
