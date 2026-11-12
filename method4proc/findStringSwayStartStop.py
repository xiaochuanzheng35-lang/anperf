import cv2
from tools import anPerfToolOcr, anPerfToolFrameProc, anPerfToolDebug
from . import perfAnaParam

class findStringStopSway(object):

    def init(self, methodConfigDict):
        self.checkDirection= methodConfigDict["direction"]
        self.threshold   = float( methodConfigDict["threshold"] )
        self.detectFrameNum = 5
        if "detectFrameNum" in methodConfigDict.keys():            self.detectFrameNum = int(methodConfigDict["detectFrameNum"])
        self.fixFrameNumber = perfAnaParam.getFixupFrameNumber(methodConfigDict)
        self.compStringPositionLst = []
        return 0

    def proc(self, procFrameList, frameIdxList, debug_level):
        for i in range(0, len(procFrameList)):
            ret = self._coreproc( procFrameList[i], frameIdxList[i], debug_level )
            if ret>0:
                return ret
        return -1

    def _coreproc(self, procframe, procframeIdx, debug_level):
        ret, encoded_image = cv2.imencode('.jpg', procframe) # encode to jpg to reduce transfer size
        retResult = anPerfToolOcr.proc(encoded_image, debug_level) ## send to OCR service to proc
        if None!=retResult:
            anPerfToolDebug.showCvImage(debug_level, procframe, procframeIdx)
            ###
            if len(self.compStringPositionLst)>=self.detectFrameNum:
                self.compStringPositionLst.pop(0)
            retX = self.extract_obvious_string_position(retResult)
            if 0!=retX:
                self.compStringPositionLst.append(retX)
                if self.find_stop_frame( debug_level ):
                    return (procframeIdx - self.detectFrameNum + 1 + self.fixFrameNum)
                else:
                    return -1
        self.compStringPositionLst = []
        return -1

    def find_stop_frame(self, debug_level):
        if self.detectFrameNum!=len(self.compStringPositionLst):
            return False
        tmpsum = 0
        for i in range(0, self.detectFrameNum-1):
            tmpsum += abs( self.compStringPositionLst[i]-self.compStringPositionLst[i+1] ) # 注：对每次相对移动的绝对值进行求和，对“抖动”产生的移动距离进行累加
        if debug_level>2:
            print( tmpsum )
        if (tmpsum)<self.threshold: # 误差阈值与检测窗口长度的关系：2.5/20帧(整体画面不抖)，3.5/20帧(整体画面有抖动)
            return True
        return False

    def extract_obvious_string_position(self, ocr_result_list):
        for r in ocr_result_list:
            if len(r["text"])>3: # Note: only calc positons of string length > 3
                if   "vertical"==self.checkDirection:
                    ret = r["cy"] #            print( r["text"] )            print(ret)
                elif "horizontal"==self.checkDirection:
                    ret = r["cx"] #            print( r["text"] )            print(ret)
                return ret
        return 0
