import os, sys, cv2
import numpy as np


def getLightness(imageframe):
    """
    Calculates the average lightness.
    """

    # 1. Convert to LAB color space
    lab = cv2.cvtColor(imageframe, cv2.COLOR_BGR2LAB)
    
    # 2. Extract the L (Lightness) channel
    l_channel, _, _ = cv2.split(lab)
    
    # 3. Return the mean lightness (0-255)
    return np.mean(l_channel)


def getLightRatio4BinaryFrame(binaryframe):
    white_count = np.sum(binaryframe == 255)
    total_pixels= binaryframe.shape[0] * binaryframe.shape[1]
    return  float(white_count / total_pixels)
