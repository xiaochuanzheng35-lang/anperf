import numpy as np
import matplotlib.pyplot as plt

def drawPlotWithDataDict(dataDict):
    ### draw the curve for analysis
    indexList = sorted( dataDict.keys() )
    valueList = []
    for i in indexList:
        valueList.append( dataDict[i] )
    x = np.array(indexList)
    y = np.array(valueList)
    plt.plot(x, y, label='change curve')
    plt.axhline(y=np.mean(y), color='r', linestyle='-', label='Mean')
    plt.legend()
    plt.show()
    input()

def drawPlotWithXYarray(Xarray, Yarray):
    print(type(Xarray[0]))
    plt.plot(Xarray, Yarray, label='change curve')
    plt.axhline(y=np.mean(Yarray), color='r', linestyle='-', label='Mean')
    plt.legend()
    plt.show()
    input()

def drawPlotWithXYarrayAndRedDotList(Xarray, Yarray, RedDotXarray, RedDotYarray):
    print(type(Xarray[0]))
    plt.plot(Xarray, Yarray, label='change curve')
    #plt.plot(min_positions, min_values, 'ro', label='bottom')
    plt.plot(RedDotXarray, RedDotYarray, 'ro', label='bottom')
    plt.axhline(y=np.mean(Yarray), color='r', linestyle='-', label='Mean')
    plt.legend()
    plt.show()
    input()

def drawPlotCurveWithIndex(datalist, indexlist):
    # 2. Create the curve plot (indices on X-axis, data on Y-axis)
    plt.plot(indexlist, datalist, linestyle='-', marker='o', color='b', label='Trend')
    # 3. Add descriptive labels and formatting
    plt.title("Curve Plot from Custom Data")
    plt.xlabel("Index")
    plt.ylabel("Value")
    plt.grid(True)
    plt.legend()
    # 4. Display the plot
    plt.show()
