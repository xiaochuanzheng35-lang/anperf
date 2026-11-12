import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim  # Remember: pip install scikit-image
from tools import anPerfToolOcr, anPerfToolKeywordsMatch, anPerfToolDebug
from . import perfAnaParam

class detectObjectMoveStartStop(object):

    def init(self, methodConfigDict):
        self.is_changing = False
        self.noise_floor_variance = None
        self.frame_history = []
        self.high_thresh=3.5
        self.low_thresh=1.2
        if "high_thresh" in methodConfigDict.keys():            self.high_thresh   = float( methodConfigDict["high_thresh"] )
        if "low_thresh" in methodConfigDict.keys():            self.low_thresh   = float( methodConfigDict["low_thresh"] )
        self.returnPoint = methodConfigDict["returnPoint"]
        if not self.returnPoint in ["start", "stop"]:
            return -1
        self.window_size = int( methodConfigDict["window_size"] )
        self.fixFrameNumber = perfAnaParam.getFixupFrameNumber(methodConfigDict)
        return 0

    def proc(self, procFrameList, frameIdxList, debug_level):
        for i in range(0, len(procFrameList)):
            ret = self._coreproc( procFrameList[i], frameIdxList[i], debug_level )
            if ret>0:
                return ret
        return -1

    def _coreproc(self, procframe, procframeIdx, debug_level):
        # 1. Isolate ROI and filter out sensor pixel noise
        gray_roi = cv2.cvtColor(procframe, cv2.COLOR_BGR2GRAY)
        blurred_roi = cv2.GaussianBlur(gray_roi, (5, 5), 0)
        # 2. Maintain a rolling temporal window
        self.frame_history.append(blurred_roi.astype(np.float32))
        if len(self.frame_history) > self.window_size:
            self.frame_history.pop(0)
        else:
            return -1 # Wait until window is full before testing variance
        # 3. Compute temporal variance across the window to absorb camera sway
        # Dynamic objects cause high variance; swaying lines cause minor local variance
        history_array = np.array(self.frame_history)
        variance_map = np.var(history_array, axis=0)
        mean_variance = np.mean(variance_map)
        # 4. Establish baseline ambient noise floor from the initial stable frames
        if self.noise_floor_variance is None:
            self.noise_floor_variance = mean_variance if mean_variance > 0.1 else 0.1
            return -1 #continue
        if debug_level>2:
            print(mean_variance)
        anPerfToolDebug.showCvImage(debug_level, procframe, procframeIdx)
        # 5. Dual-Threshold Hysteresis Logic
        if not self.is_changing: # Case A: Currently quiet. Check if change starts.
            if mean_variance > (self.noise_floor_variance * self.high_thresh):
                self.is_changing = True
                start_frame = (procframeIdx + self.fixFrameNumber)
                print(f"▶️ CHANGE STARTED at Frame: {start_frame} (Variance Spike: {mean_variance:.2f})")
                if "start"==self.returnPoint:
                    return start_frame
        else:  # Case B: Currently active. Check if change stops.
            if mean_variance < (self.noise_floor_variance * self.low_thresh):
                self.is_changing = False
                stop_frame = (procframeIdx + self.fixFrameNumber)
                print(f"⏹️ CHANGE STOPPED at Frame: {stop_frame} (Variance Settled: {mean_variance:.2f})")
                return stop_frame
        # 6. Adaptively update noise floor slowly ONLY when things are quiet
        if not self.is_changing:
            self.noise_floor_variance = 0.95 * self.noise_floor_variance + 0.05 * mean_variance
        return -1
