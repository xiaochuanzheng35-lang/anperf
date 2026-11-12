import numpy as np
import pandas as pd

def filter(data_list, window_1=5, window_2=3):
    df = pd.DataFrame({"Speed": data_list})
    # =========================================================================
    # STAGE 1: Course Filter (Adaptive to any scale)
    # =========================================================================
    #window_1 = 5
    median_1 = df["Speed"].rolling(window=window_1, center=True, min_periods=1).median()
    abs_dev_1 = (df["Speed"] - median_1).abs()
    mad_1 = abs_dev_1.rolling(window=window_1, center=True, min_periods=1).median()
    
    mad_score_1 = 0.6745 * abs_dev_1 / (mad_1 + 1e-8) # Lowered floor protection to 1e-8 for small numbers
    
    # SCALE-INVARIANT RULES:
    is_directional_flip = (np.sign(df["Speed"]) != np.sign(median_1)) & (df["Speed"] != 0) & (median_1 != 0)
    
    # Replaced " > 3.0" with a relative rule: Deviation cannot be greater than 60% of the local median speed
    is_sudden_jump = abs_dev_1 > (0.60 * median_1.abs()) 
    
    is_noise_1 = (mad_score_1 > 2.2) | is_directional_flip | is_sudden_jump
    df["Stage1_Cleaned"] = df["Speed"].where(~is_noise_1, np.nan).interpolate()
    # =========================================================================
    # STAGE 2: Fine Filter (Adaptive to any scale)
    # =========================================================================
    #window_2 = 3
    median_2 = df["Stage1_Cleaned"].rolling(window=window_2, center=True, min_periods=1).median()
    abs_dev_2 = (df["Stage1_Cleaned"] - median_2).abs()
    mad_2 = abs_dev_2.rolling(window=window_2, center=True, min_periods=1).median()
    
    mad_score_2 = 0.6745 * abs_dev_2 / (mad_2 + 1e-8)
    
    is_noise_2 = mad_score_2 > 1.2 # Uniform threshold holds true here!
    df["Stage2_Strict_Cleaned"] = df["Stage1_Cleaned"].where(~is_noise_2, np.nan).interpolate()
    return df["Stage2_Strict_Cleaned"].tolist()

## Microscopic test data
#speed_data = [0, 0.001, 0.001, 0.002, 0.003, -0.001, 0.003, 0.004, 0.005, -0.002, 0.006, 0.002, 0.006, -0.001, 0.004, 0.003, 0.002, 0.001, 0, 0, 0, 0]
#filtered_data = filter(speed_data, 5, 3)
#print("Original Raw Data:      ", [round(x, 4) for x in speed_data])
#print("Stage 2 (Strict Clean): ", [round(x, 4) for x in filtered_data])
