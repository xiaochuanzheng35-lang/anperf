import cv2
from tools import anPerfToolOcr, anPerfToolKeywordsMatch, anPerfToolDebug
from . import perfAnaParam

class findAreaString(object):

    def init(self, methodConfigDict):
        self.returnPoint = perfAnaParam.getReturnPoint(methodConfigDict, "appear")
        if not self.returnPoint in ["disappear", "appear"]:
            return -1
        self.characterCount = perfAnaParam.getCharacterCount(methodConfigDict)
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
        retResult = anPerfToolOcr.proc(encoded_image, debug_level) ## send to OCR service to proc        #print(retResult)
        if None!=retResult:
            anPerfToolDebug.showCvImage(debug_level, procframe, procframeIdx)
            if self.returnPoint=="appear":
                if len(retResult)>0:
                    if self.getCharacterCount(retResult, debug_level)>=(self.characterCount + 1):
                        return (procframeIdx + self.fixFrameNumber)  # get return frame index with fixup
            else:
                if len(retResult)==0: # return if no string
                    return (procframeIdx + self.fixFrameNumber)
                elif self.characterCount>0 and (self.getCharacterCount(retResult, debug_level)<=self.characterCount): # return if area character number less than specified count
                    return (procframeIdx + self.fixFrameNumber)  # get return frame index with fixup
        return -1

    def getCharacterCount(self, ocr_result_list, debug_level):
        character_number = 0
        for item in ocr_result_list:
            tmpstr = item["text"]
            character_number += len(tmpstr)
        if debug_level>2:
            print(f"get character number = {character_number}")
        return character_number
