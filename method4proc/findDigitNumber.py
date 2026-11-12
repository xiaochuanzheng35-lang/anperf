import cv2
from tools import anPerfToolOcr, anPerfToolDebug
from . import perfAnaParam

class findDigitNumber(object):

    def init(self, methodConfigDict):
        self.checkDigit = perfAnaParam.getReturnPoint(methodConfigDict, "zero")
        if not self.checkDigit in ["zero", "non-zero"]:
            return -1
        self.digitNumThreshold   = int( methodConfigDict["digitNumThreshold"] )
        self.zeroNumberUplimit = 60000
        if "zeroNumberUplimit" in methodConfigDict.keys():            self.zeroNumberUplimit = methodConfigDict["zeroNumberUplimit"]
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
            zeroDigitNum,noneZeroDigitNum = self.count_digits(retResult, debug_level):
            if self.checkDigit=="zero":
                if zeroDigitNum>=self.digitNumThreshold:
                    if zeroDigitNum<=self.zeroNumberUplimit:
                        if debug_level>1:
                            print(f"find non-zero ({noneZeroDigitNum}), zero ({zeroDigitNum})")
                            print(ocr_result_list)
                        return (procframeIdx + self.fixFrameNum) # get return frame index with fixup
            else:
                if noneZeroDigitNum>=self.digitNumThreshold:
                    if debug_level>1:
                        print(f"find non-zero ({noneZeroDigitNum}), zero ({zeroDigitNum})")
                        print(ocr_result_list)
                    return (procframeIdx + self.fixFrameNum) # get return frame index with fixup                
        return -1

    def count_digits(self, ocr_result_list, debug_level):
        zeroDigitNum = 0
        noneZeroDigitNum = 0
        for item in ocr_result_list:
            tmpstr = item["text"]        # noneZeroDigitNum = 0 #sum( c.isdigit() for c in tmpstr)
            for c in tmpstr:
                if c.isdigit() and (int(c)>0):
                    noneZeroDigitNum += 1
                elif c in "bSs": # 防止 OCR 将数字 5 识别为 S或s
                    noneZeroDigitNum += 1
                elif c in "0OoD":
                    zeroDigitNum += 1
        if debug_level>2:
            print(f"find non-zero ({noneZeroDigitNum}), zero ({zeroDigitNum})")
        return zeroDigitNum,noneZeroDigitNum

    def has_zero_digits(self, ocr_result_list, debug_level):
        zeroDigitNum = 0
        for item in ocr_result_list:
            tmpstr = item["text"]        # noneZeroDigitNum = 0 #sum( c.isdigit() for c in tmpstr)
            for c in tmpstr:
                if c.isdigit() and (int(c)==0):                zeroDigitNum += 1
        if zeroDigitNum>=self.digitNumThreshold:
            if debug_level>1:
                print(f"find zero ({zeroDigitNum})")
                print(ocr_result_list)
            return True
        if debug_level>2:
            print(f"find zero ({zeroDigitNum})")
        return False
