import os, cv2
from tools import anPerfToolDebug

class rotate90counterclockwise(object):

    def proc(self, procframe, debug_level):
        retframe = cv2.rotate(procframe, cv2.ROTATE_90_COUNTERCLOCKWISE)
        anPerfToolDebug.showCvImage(debug_level, retframe, 0)
        return retframe
