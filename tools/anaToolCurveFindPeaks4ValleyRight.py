from scipy.signal import find_peaks

def find_peaks_around_specValley_scipy(specValleyIndex, y, heightThreshold):
    if heightThreshold>0:
        peaks, _ = find_peaks( y, heightThreshold )
    else:
        peaks, _ = find_peaks( y)
    left  = peaks[ peaks < specValleyIndex ]
    right = peaks[ peaks > specValleyIndex ]
    if left.size:
        retLeftPeak = left[-1]
    else:
        retLeftPeak = None
    if right.size:
        retRightPeak = right[0]
    else:
        retRightPeak = None
    return retLeftPeak, retRightPeak
