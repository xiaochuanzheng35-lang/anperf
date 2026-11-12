import cv2
from tools import anPerfToolOcr, anPerfToolKeywordsMatch, anPerfToolDebug
from . import perfAnaParam

class findKeywords(object):

    def init(self, methodConfigDict):
        self.keywordList = methodConfigDict["keywordList"]
        if len(self.keywordList)==0:
            print("Error: no keyword list found!")
            return -1
        self.threshold   = perfAnaParam.getThreshold(methodConfigDict)
        self.returnPoint = perfAnaParam.getReturnPoint(methodConfigDict, "appear")
        if not self.returnPoint in ["disappear", "appear"]:
            return -1
        self.fixFrameNumber = perfAnaParam.getFixupFrameNumber(methodConfigDict)
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
            if self.returnPoint=="appear":
                return self.find_keywords_appear(retResult, procframeIdx, debug_level)
            else:
                return self.find_keywords_disappear(retResult, procframe, procframeIdx, debug_level)
        return -1

    def find_keywords_appear(self, ocr_result_list, procframeIdx, debug_level):
        # check if match the threshold
        if anPerfToolKeywordsMatch.find_match_frame(ocr_result_list, self.keywordList, self.threshold):
            return (procframeIdx + self.fixFrameNumber)  # get return frame index with fixup
        return -1

    def find_keywords_disappear(self, ocr_result_list, procframe, procframeIdx, debug_level):
        # check if match the threshold
        if not anPerfToolKeywordsMatch.find_match_frame(ocr_result_list, self.keywordList, self.threshold):
            # do a retry to confirm
            #print("\n!!! findKeywordsDisappear do a retry to confirm !!!\n")
            procframe = cv2.fastNlMeansDenoising(procframe, None, h=10, templateWindowSize=7, searchWindowSize=21)
            ret, encoded_image = cv2.imencode('.jpg', procframe) # encode to jpg to reduce transfer size
            retResult = anPerfToolOcr.proc(encoded_image, debug_level) ## send to OCR service to proc
            if None!=retResult:
                anPerfToolDebug.showCvImage(debug_level, procframe, procframeIdx)
                # check if match the threshold
                if not anPerfToolKeywordsMatch.find_match_frame(retResult, self.keywordList, self.threshold):
                    return (procframeIdx + self.fixFrameNumber)  # get return frame index with fixup
        return -1
