import cv2
from tools import anPerfToolFrameGetLightness, anPerfToolDebug
from . import perfAnaParam

class detectLightnessChange(object):

    def init(self, methodConfigDict):
        self.threshold   = float( methodConfigDict["threshold"] )
        self.detectFrameNum = perfAnaParam.getDetectFrameNumber(methodConfigDict) #5
        self.fixFrameNumber = perfAnaParam.getFixupFrameNumber(methodConfigDict)
        self.calcLightnessLst = []
        return 0

    def proc(self, procFrameList, frameIdxList, debug_level):
        for i in range(0, len(procFrameList)):
            ret = self._coreproc( procFrameList[i], frameIdxList[i], debug_level )
            if ret>0:
                return ret
        return -1

    def _coreproc(self, procframe, procframeIdx, debug_level):
        anPerfToolDebug.showCvImage(debug_level, procframe, procframeIdx)
        retLightness = anPerfToolFrameGetLightness.getLightness(procframe)        #print(f"detectLightnessChange - get current frame lightness = {retLightness}")
        self.calcLightnessLst.append( retLightness )
        if len(self.calcLightnessLst)>self.detectFrameNum:
            self.calcLightnessLst.pop(0)            #print(self.calcLightnessLst)
            lightnessGap = (self.calcLightnessLst[-1] - self.calcLightnessLst[0])
            if debug_level>2:
                print(lightnessGap)
            if self.threshold>0:
                if lightnessGap>=self.threshold:
                    return (procframeIdx + self.fixFrameNumber)
            else:
                if lightnessGap<self.threshold:
                    return (procframeIdx + self.fixFrameNumber)
        return -1
