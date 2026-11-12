import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

def detect_and_plot_extrema(index_list, data_list, debug_level, mean_value=None):
    """
    Finds peaks and valleys in the data using scipy.signal.find_peaks
    and renders them immediately on a clean matplotlib plot.
    """
    x = np.array(index_list)
    y = np.array(data_list)
    # 1. Detect Peaks and Valleys (adjust prominence/distance for noise control)
    peak_indices, _ = find_peaks(y, distance=10, prominence=0.0001)
    valley_indices, _ = find_peaks(-y, distance=10, prominence=0.0001)
    if debug_level>2:
        # 2. Initialize the plot layout
        plt.figure(figsize=(8, 6))
        # Plot the original signal curve
        plt.plot(x, y, label='change curve', color='tab:blue', linewidth=2)
        # Plot the mean reference line (calculate if not provided explicitly)
        ref_mean = mean_value if mean_value is not None else np.mean(y)
        plt.axhline(y=ref_mean, color='red', linestyle='-', label='Mean')
        # 3. Draw the markers on top of the curve
        if len(peak_indices) > 0:
            plt.scatter(x[peak_indices], y[peak_indices], 
                        color='forestgreen', marker='^', s=100, zorder=5, label='Peaks')
        if len(valley_indices) > 0:
            plt.scatter(x[valley_indices], y[valley_indices], 
                        color='darkorange', marker='v', s=100, zorder=5, label='Bottoms')
        # 4. Text Annotations for the primary significant waves
        for idx in peak_indices:
            if y[idx] > 0.00075:  # Target the major positive crest
                plt.annotate(f"Peak\n({x[idx]}, {y[idx]:.4f})", (x[idx], y[idx]),
                             textcoords="offset points", xytext=(0, 10), ha='center', weight='bold')
        for idx in valley_indices:
            if y[idx] < -0.0010:  # Target the extreme big wave plunge
                plt.annotate(f"Valley Bottom\n({x[idx]}, {y[idx]:.4f})", (x[idx], y[idx]),
                             textcoords="offset points", xytext=(0, -25), ha='center', weight='bold')
        # 5. Graph styling details
        plt.title("Extrema Detection Analysis")
        plt.xlabel("Index")
        plt.ylabel("Value")
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.legend(loc='upper left')
        # Display the final image
        plt.show()
    
    # Return coordinates back to your program in case you need them for further math
    return {
        "peaks": list(zip(x[peak_indices], y[peak_indices])),
        "valleys": list(zip(x[valley_indices], y[valley_indices]))
    }

# --- Example Usage ---
# found_coords = detect_and_plot_extrema(index, gap_speed)
