import os, cv2

import numpy as np

from tools import anPerfToolDebug

class rotate180(object):

    def proc(self, procframe, debug_level):
        if procframe is None or not isinstance(procframe, np.ndarray):
            print("输入帧无效")
            return procframe

        rotated_img = cv2.rotate(procframe, cv2.ROTATE_180)

        anPerfToolDebug.showCvImage(debug_level, rotated_img, 0)

        return rotated_img

