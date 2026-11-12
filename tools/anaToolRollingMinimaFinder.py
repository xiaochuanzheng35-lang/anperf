import numpy
import matplotlib.pyplot as plt

def rolling_minima(y, threshold=0.7, win=15):
    pad = win
    y_pad = numpy.pad(y, pad_width=pad, mode='edge')
    idx = []
    for i in range(pad, len(y_pad) - pad):
        w = y_pad[ i - pad:i + pad + 1]
        if w[pad] == numpy.min(w):
            if w[pad]<threshold:
                idx.append(i-pad)
    idx = numpy.array(idx)
    return idx[numpy.diff(numpy.hstack(([False],idx))) != 0]
