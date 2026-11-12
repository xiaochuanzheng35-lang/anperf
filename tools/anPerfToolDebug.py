import cv2

def printData(debug_level, dataToPrint, describeString=""):
    if debug_level>0:
        if len(describeString)>0:            print( describeString )
        print( dataToPrint )

def printDataAndWaitForInput(debug_level, dataToPrint, describeString=""):
    if debug_level>0:
        printData(debug_level, dataToPrint, describeString)
    if debug_level>1:
        input()

def showCvImage(debug_level, image_frame_data, frame_index):
    if debug_level>0:
        if debug_level>2:
            print(f"Frame index = {frame_index}")
        cv2.imshow('Processed Frame', image_frame_data) # 显示处理后的帧，当用户按下q键时，退出循环
        if cv2.waitKey(1) & 0xFF == ord('q'):
            return -1
