import cv2
from tools import anPerfToolCvSSIMmatcher, anPerfToolDebug
from . import perfAnaParam

class findAreaDiffBySsim(object):

    def init(self, methodConfigDict):
        self.first_frame_gray = None
        self.similarThreshold = 0.8
        if "similarThreshold" in methodConfigDict.keys():            self.similarThreshold   = float( methodConfigDict["similarThreshold"] )
        self.fixFrameNumber = perfAnaParam.getFixupFrameNumber(methodConfigDict)
        return 0

    def proc(self, procFrameList, frameIdxList, debug_level):
        for i in range(0, len(procFrameList)):
            ret = self._coreproc( procFrameList[i], frameIdxList[i], debug_level )
            if ret>0:
                return ret
        return -1

    def _coreproc(self, procframe, procframeIdx, debug_level):
        if self.first_frame_gray is None:
            ref_gray = cv2.cvtColor(procframe, cv2.COLOR_BGR2GRAY)
            self.first_frame_gray = cv2.GaussianBlur(ref_gray, (5, 5), 0)
            return -1
        current_gray = cv2.cvtColor(procframe, cv2.COLOR_BGR2GRAY)
        score = anPerfToolCvSSIMmatcher.calc_match_score(self.first_frame_gray, current_gray, debug_level)
        if debug_level>2:
            print(f"Similarity score = {score}")
        anPerfToolDebug.showCvImage(debug_level, procframe, procframeIdx)
        # 4. Handle Alerts
        if score < self.similarThreshold:
            print(f"⚠️ Frame {procframeIdx}: Structural Change! (Similarity: {score:.4f})")
            return (procframeIdx + self.fixFrameNumber)  # get return frame index with fixup
        return -1
