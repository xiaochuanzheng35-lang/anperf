import cv2, numpy


def has_line_simple(img, debug_level=0, specLineNumArray=[1,1], min_len=80, canny_th1=50, canny_th2=150):
    gray  = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, canny_th1, canny_th2)
    if debug_level>1:
        cv2.imshow('edges', edges)
    lines = cv2.HoughLinesP(edges, 1, numpy.pi/180, 60, minLineLength=min_len, maxLineGap=5)
    if lines is None:
        return False
    lineNum = len(lines)
    if lineNum>=specLineNumArray[0] and lineNum<=specLineNumArray[1]:
        return True
    return False
    #return bool(lines is not None and len(lines)>=threshold)
