import cv2
import numpy as np
from tools import anPerfToolDebug

def calcFlow_AverageMovement_norm(lastframe, inputframe, direction="horizontal", debug_level=0):
    frames = [lastframe, inputframe]
    threshold = 1.0
    distances = []
    if len(frames) < 2:
        return 0
    prev_gray = cv2.cvtColor(frames[0], cv2.COLOR_BGR2GRAY)
    # Determine vector index: 0 for X (horizontal), 1 for Y (vertical)
    axis_idx = 0 if direction == "horizontal" else 1
    for i in range(1, len(frames)):
        curr_gray = cv2.cvtColor(frames[i], cv2.COLOR_BGR2GRAY)
        flow = cv2.calcOpticalFlowFarneback(
            prev_gray, curr_gray, None, 0.5, 3, 15, 3, 5, 1.2, 0
        )
        # 1. Isolate the chosen axis
        flow_vec = flow[..., axis_idx]
        # 2. Filter noise
        mag = np.abs(flow_vec)
        motion_mask = mag > threshold
        if np.any(motion_mask):
            # 3. Average the vectors
            # Horizontal: Left (-) becomes (+), Right (+) becomes (-)
            # Vertical: Up (-) becomes (+), Down (+) becomes (-)
            avg_dist = -np.mean(flow_vec[motion_mask])
        else:
            avg_dist = 0.0
        distances.append(float(avg_dist))
        prev_gray = curr_gray
    if debug_level > 2:
        for i, d in enumerate(distances):
            print(f"dir={direction}, distance={d:.3f}")
    return distances[0]

def calcFlow_AverageMovement_240FPS(lastframe, inputframe, direction="horizontal", debug_level=0):
    """
    Optimized for high frame-rate (240 FPS) video tracking.
    
    NOTE: To get reliable results at 240 FPS, you should ideally pass frames
    that are spaced 4 to 8 frames apart. If you must pass sequential frames, 
    we use extreme filtering below.
    """
    stride_counter=0
    # 1. Convert to grayscale and apply heavy blur to kill 240FPS sensor hiss
    prev_gray = cv2.cvtColor(lastframe, cv2.COLOR_BGR2GRAY)
    prev_gray = cv2.GaussianBlur(prev_gray, (7, 7), 0)
    curr_gray = cv2.cvtColor(inputframe, cv2.COLOR_BGR2GRAY)
    curr_gray = cv2.GaussianBlur(curr_gray, (7, 7), 0)
    # 2. Farneback parameters tuned for micro-movements & high noise stability
    flow = cv2.calcOpticalFlowFarneback(
        prev_gray, curr_gray, None, 
        pyr_scale=0.5, 
        levels=4,        # Deeper pyramid levels
        winsize=31,      # Large window averaging to overpower pixel-level noise
        iterations=3, 
        poly_n=7,        # Larger pixel neighborhood
        poly_sigma=1.5, 
        flags=0
    )
    # 3. Isolate direction axis (0 for X, 1 for Y)
    axis_idx = 0 if direction == "horizontal" else 1
    flow_vec = flow[..., axis_idx]
    # 4. Filter Noise
    # At 240FPS, true physical motion is tiny. We lower the threshold,
    # but we zero out the noisy pixels completely instead of dropping them from the mean.
    mag = np.abs(flow_vec)
    subpixel_noise_floor = 0.15  # Pixels moving less than 0.15 are forced to 0.0
    
    clean_flow_vec = np.where(mag > subpixel_noise_floor, flow_vec, 0.0)
    # 5. Global movement metric calculation
    # Averaging the whole frame ensures local noise cancellations balance out
    avg_dist = -np.mean(clean_flow_vec)
    if debug_level > 2:
        print(f"dir={direction}, 240FPS adjusted distance={avg_dist:.4f}")
    return float(avg_dist)