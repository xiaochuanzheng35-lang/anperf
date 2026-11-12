import cv2, time, numpy
from tools import anPerfToolFrameGetLightness, anPerfToolDebug, anaToolFilterGaussian, anaToolDrawPlot, anaToolCurveBottomPeak, anaTool4ChangeData, anaToolFilterAverage #anaToolFilter2StagesMadInterpolation
from . import perfAnaParam

class detectOtsuBinaryLightnessChange(object):

    def init(self, methodConfigDict):
        self.threshold   = float( methodConfigDict["threshold"] )
        self.detectFrameNum = perfAnaParam.getDetectFrameNumber(methodConfigDict) #5
        self.fixFrameNumber = perfAnaParam.getFixupFrameNumber(methodConfigDict)
        self.changeTrend = perfAnaParam.getChangeTrend(methodConfigDict, "speed")
        if not self.changeTrend in ["speed", "acceleration", "none"]:
            return -1
        self.lightnessList = []
        self.frameIndexLst = []
        self.cachedGap = []
        return 0

    def proc(self, procFrameList, frameIdxList, debug_level):
        for i in range(0, len(procFrameList)):
            self.lightnessList.append(self._getBinaryLightnessRatio(procFrameList[i], frameIdxList[i], debug_level))
            self.frameIndexLst.append(frameIdxList[i])
        if self.changeTrend=="speed":
            tmpData_list,anaIndexlist = anaToolFilterGaussian.filter_with_mask(self.lightnessList, self.frameIndexLst, debug_level)
            anaDatalist,anaIndexlist  = anaTool4ChangeData.getChangeSpeed(tmpData_list, anaIndexlist, self.detectFrameNum, debug_level)
        elif self.changeTrend=="acceleration":
            tmpData_list,anaIndexlist = anaToolFilterGaussian.filter_with_mask(self.lightnessList, self.frameIndexLst, debug_level)
            #tmpData_list,anaIndexlist = anaToolFilterAverage.filter(self.lightnessList, self.frameIndexLst, 7) #anaToolFilter2StagesMadInterpolation
            #if debug_level > 1:                anaToolDrawPlot.drawPlotWithXYarray(numpy.array(anaIndexlist), numpy.array(tmpData_list))
            anaDatalist,anaIndexlist  = anaTool4ChangeData.getChangeAcceleration(tmpData_list, anaIndexlist, debug_level)
        else: # lightness ratio
            anaDatalist = self.lightnessList
            anaIndexlist= self.frameIndexLst
            if debug_level > 1:                anaToolDrawPlot.drawPlotWithXYarray(numpy.array(anaIndexlist), numpy.array(anaDatalist))
        for i in range(0, len(anaIndexlist)):
            if self.threshold>0:
                if anaDatalist[i]>self.threshold:                    return (anaIndexlist[i] + self.fixFrameNumber)
            else:
                if anaDatalist[i]<self.threshold:                    return (anaIndexlist[i] + self.fixFrameNumber)
        #anaToolCurveBottomPeak.detect_and_plot_extrema(index_list, filtered_lightness_datalist, debug_level)
        return -1

    def _getBinaryLightnessRatio(self, procframe, procframeIdx, debug_level):
        if len(procframe.shape) == 3:
            procframe = cv2.cvtColor(procframe, cv2.COLOR_BGR2GRAY)
        # Otsu 
        _, gray = cv2.threshold(procframe, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        anPerfToolDebug.showCvImage(debug_level, gray, procframeIdx)
        return anPerfToolFrameGetLightness.getLightRatio4BinaryFrame(gray)
