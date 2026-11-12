import cv2
import numpy as np
from tools import anaToolCalcAcceleration, anPerfToolDebug
from . import perfAnaParam

class detectMoveByOpticalFlowAcceleration(object):

    def init(self, methodConfigDict):
        self.direction   = methodConfigDict["direction"]
        self.returnPoint = methodConfigDict["returnPoint"]
        self.threshold   = float( methodConfigDict["threshold"] )
        self.detectFrameNum = 5
        if "detectFrameNum" in methodConfigDict.keys():            self.detectFrameNum = int(methodConfigDict["detectFrameNum"])
        self.fixFrameNumber = perfAnaParam.getFixupFrameNumber(methodConfigDict)
        self.compMoveList = []
        self.lastFrame   = None
        return 0

    def proc(self, procFrameList, frameIdxList, debug_level):
        for i in range(0, len(procFrameList)):
            ret = self._coreproc( procFrameList[i], frameIdxList[i], debug_level )
            if ret>0:
                return ret
        return -1

    def _coreproc(self, procframe, procframeIdx, debug_level):
        if self.lastFrame is None:
            self.lastFrame = procframe
            return -1
        moveDistance = self.calcFlow_AverageMovement(procframe, self.direction, debug_level)
        anPerfToolDebug.showCvImage(debug_level, procframe, procframeIdx)
        self.compMoveList.append(moveDistance)
        if len(self.compMoveList)>=self.detectFrameNum:
            self.compMoveList.pop(0)
        else:
            return -1
        accelerations = anaToolCalcAcceleration.calculate_displaced_kinematics(self.compMoveList, 1)
        if debug_level>2:
            print(f"acceleration = {accelerations[-1]}")
        if self.returnPoint=="start":
            if self.threshold>0:
                if accelerations[-1]>self.threshold:
                    return (procframeIdx + self.fixFrameNumber)
            else:
                if accelerations[-1]<self.threshold:
                    return (procframeIdx + self.fixFrameNumber)
        else:
            if abs(accelerations[-1])<abs(self.threshold):
                return (procframeIdx + self.fixFrameNumber)
        return -1

    def calcFlow_AverageMovement(self, inputframe, direction="horizontal", debug_level=0):
        frames = [self.lastFrame, inputframe]
        threshold = 1.0
        distances = []
        if len(frames) < 2:
            return distances
        prev_gray = cv2.cvtColor(frames[0], cv2.COLOR_BGR2GRAY)
        # Determine vector index: 0 for X (horizontal), 1 for Y (vertical)
        axis_idx = 0 if direction == "horizontal" else 1
        for i in range(1, len(frames)):
            curr_gray = cv2.cvtColor(frames[i], cv2.COLOR_BGR2GRAY)
            flow = cv2.calcOpticalFlowFarneback(
                prev_gray, curr_gray, None, 0.5, 3, 15, 3, 5, 1.2, 0
            )
            # 1. Isolate the chosen axis
            flow_vec = flow[..., axis_idx]
            # 2. Filter noise
            mag = np.abs(flow_vec)
            motion_mask = mag > threshold
            if np.any(motion_mask):
                # 3. Average the vectors
                # Horizontal: Left (-) becomes (+), Right (+) becomes (-)
                # Vertical: Up (-) becomes (+), Down (+) becomes (-)
                avg_dist = -np.mean(flow_vec[motion_mask])
            else:
                avg_dist = 0.0
            distances.append(float(avg_dist))
            prev_gray = curr_gray
        if debug_level > 3:
            for i, d in enumerate(distances):
                print(f"dir={direction}, distance={d:.3f}")
        return distances[0]
