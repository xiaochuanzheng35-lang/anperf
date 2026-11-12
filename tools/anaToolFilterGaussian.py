import numpy
from tools import anPerfToolDebug, anaToolDrawPlot

def proc(xArray, yArray, debug_level):
    filterWeightList = [0.1, 0.15, 0.5, 0.15, 0.1] # gaussian filter config
    #filterWeightList = [0.02, 0.08, 0.8, 0.08, 0.02] # gaussian filter config
    #filterWeightList = [0.0, 0.05, 0.9, 0.05, 0.0] # gaussian filter config
    stripLen = int(len(filterWeightList)/2)
    #print(filterWeightList)
    # init working avg window and start processing
    kernel = numpy.array(filterWeightList)
    smoothedArray = numpy.convolve(yArray, kernel, mode='same')
    smoothedList  = smoothedArray.tolist()
    if debug_level > 1: # plot smoothed curve
        anaToolDrawPlot.drawPlotWithXYarray(xArray, smoothedArray)
    return xArray[0 : -stripLen], smoothedArray[0 : -stripLen]

def filter_with_mask(data_list, index_list, debug_level, sigma=1.5, radius=2, padding_value=0.0):
    """
    Applies a Gaussian filter using internal reflection padding,
    then overwrites edge-distorted boundary points with -1.
    """
    raw_data = numpy.array(data_list, dtype=float)
    # 1. Create a symmetric 1D Gaussian kernel
    x = numpy.arange(-radius, radius + 1)
    kernel = numpy.exp(-x**2 / (2 * sigma**2))
    kernel /= kernel.sum()  # Normalize so the sum of weights equals 1
    # 2. Auto-select internal data as padding (Reflect boundary values)
    # This ensures the window has real numeric context during convolution
    padded_data = numpy.pad(raw_data, radius, mode='reflect')
    # 3. Apply the Gaussian filter via 1D convolution
    filtered_data = numpy.convolve(padded_data, kernel, mode='valid')
    # 4. Explicitly mark the edge/padding regions as -1
    #filtered_data[:radius] = padding_value #-1.0
    #filtered_data[-radius:] = padding_value #-1.0
    retData = numpy.round(filtered_data[radius:-radius], 5)
    retIndex= index_list[radius:-radius]
    if debug_level > 1: # plot curve
        idx_data = numpy.array(retIndex, dtype=int)
        anaToolDrawPlot.drawPlotWithXYarray(idx_data, retData)
    return retData.tolist(),retIndex
