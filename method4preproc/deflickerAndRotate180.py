import os, cv2
import numpy as np
from tools import anPerfToolDebug


class deflickerAndRotate180(object):
    def __init__(self):
        self.windowSize = 5
        self.framesList = []

    def proc(self, procframe, debug_level):
        procframe = cv2.rotate(procframe, cv2.ROTATE_180)
        self.framesList.append(procframe.astype(np.float32))
        if len(self.framesList) > self.windowSize:
            self.framesList.pop(0)
        # Average the frames in the buffer
        if len(self.framesList) == self.windowSize:
            return  np.mean(self.framesList, axis=0).astype(np.uint8)
        else:
            return procframe
