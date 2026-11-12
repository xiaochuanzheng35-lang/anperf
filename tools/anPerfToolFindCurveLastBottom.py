import os, cv2
import numpy as np

def findCurveBottomIndiceList(dataLst, window_size, threshold=0.88):
    min_indices = []
    for i in range(window_size // 2, len(dataLst) - window_size // 2):
        window = dataLst[i - window_size // 2:i + window_size // 2 + 1]
        if dataLst[i] == np.min(window):
            #print("find bottom in window")
            #print(dataLst[i])
            if dataLst[i]<threshold:
                min_indices.append(i)
    return min_indices

def findCurveLastBottomIndex(dataLst, window_size):
    min_indices = findCurveBottomIndiceList(dataLst, window_size)
    if len(min_indices)>0:
        return min_indices[-1]
    return -1

def findCurveFirstTop(dataLst):
    arr = np.array(dataLst)
    # 找到数组中的最大值
    max_value = np.max(arr)
    # 找到最大值的索引位置
    max_index = np.argmax(arr)
    return max_index
