import numpy
from tools import anaToolDrawPlot


def getChangeSpeed(data_list, index_list, length=3, debug_level=0):
    #length = 3  # Calculate speed across a 3-step gap (e.g., data[3] - data[0])
    data = numpy.array(data_list)
    index= numpy.array(index_list[length:])
    # Subtract the start of the window from the end of the window
    tmp_speed = data[length:] - data[:-length]
    gap_speed = numpy.round(tmp_speed, 5)
    if debug_level > 1:
        anaToolDrawPlot.drawPlotWithXYarray(index, gap_speed)
    return gap_speed.tolist(), index_list[length:]


def getChangeAcceleration(data_list, index_list, debug_level=0):
    order_length = 2  # Calculate the 2nd order difference (differences of differences)
    data = numpy.array(data_list)
    index= numpy.array(index_list[order_length:])
    tmp_speed = numpy.diff(data, n=order_length)
    order_speed = numpy.round(tmp_speed, 5)
    if debug_level > 1:
        anaToolDrawPlot.drawPlotWithXYarray(index, order_speed)
    return order_speed.tolist(), index_list[order_length:]

