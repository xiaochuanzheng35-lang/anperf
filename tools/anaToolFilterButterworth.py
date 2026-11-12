import numpy
from scipy.signal import butter, filtfilt
from tools import anPerfToolDebug, anaToolDrawPlot

def proc(xArray, yArray, debug_level):
    fs      = 1.0      # sampling frequency
    cutoff  = 0.05     # cutoff frequency to keep
    b,a = butter(N=4, Wn=cutoff/0.5*fs, btype='low')
    smooth = filtfilt(b, a, yArray)
    #return xArray, smooth
    #return xArray[0 : -stripLen], smooth[0 : -stripLen]
    #paddingLen = min(35, int(len(yArray)*0.1))
    paddingLen = min(16, int(len(yArray)*0.1))
    retXarray = xArray[0 : -paddingLen]
    retYarray = smooth[0 : -paddingLen]
    retYarray[0:paddingLen] = 0.95
    if debug_level > 1: # plot smoothed curve
        anaToolDrawPlot.drawPlotWithXYarray(retXarray, retYarray)
    return retXarray,retYarray,paddingLen
