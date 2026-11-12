import os, cv2, numpy
from tools import anCompToolCalcFrameSiftList, anCompToolFilterCurve, anaToolDrawPlot, anCompToolFindCurveBottoms, anaToolCurveFindPeaksNearValley
from . import perfAnaParam

class areaChangePlotBySift(object):
    def init(self, methodConfigDict):
        self.curveBottomPosition = methodConfigDict["curveBottomPosition"]
        if not self.curveBottomPosition in ["first", "last"]:
            return -1
        self.returnPoint = methodConfigDict["returnPoint"]
        if not self.returnPoint in ["start", "startAtMid", "default", "stopAtMid", "stop"]:
            return -1
        self.rollWinSize = int( methodConfigDict["rollingWindowSize"] )
        self.threshold   = float( methodConfigDict["bottomThreshold"] )
        self.curveBottomMinNum = 1
        if "curveBottomMinNumber" in methodConfigDict.keys():            self.curveBottomMinNum = int( methodConfigDict["curveBottomMinNumber"] )
        self.peakThreshold = -1
        if "peakThreshold" in methodConfigDict.keys():            self.peakThreshold = float( methodConfigDict["peakThreshold"] )
        self.fixFrameNumber = perfAnaParam.getFixupFrameNumber(methodConfigDict)
        return 0

    def proc(self, compFrameLst, frameIdxList, debug_level):
        (indexList, ratioList) = anCompToolCalcFrameSiftList.proc1(compFrameLst, frameIdxList, debug_level)
        if len(indexList)==0 or len(ratioList)==0 or (len(indexList)!=len(ratioList)):
            return -1
        # filter the curve
        filterOutXarray,filterOutYarray,paddingLen = anCompToolFilterCurve.proc(numpy.array(indexList), numpy.array(ratioList), debug_level)
        # find bottoms in curve
        bottomIdxList  = anCompToolFindCurveBottoms.proc( filterOutYarray, paddingLen, self.threshold, self.curveBottomMinNum, self.rollWinSize, debug_level )
        if len(bottomIdxList)<=0:
            return -1
        if debug_level > 1:
            min_positions = filterOutXarray[ bottomIdxList ]
            min_values    = filterOutYarray[ bottomIdxList ]
            anaToolDrawPlot.drawPlotWithXYarrayAndRedDotList(filterOutXarray,filterOutYarray,min_positions,min_values)
        if self.curveBottomPosition=="first":        # get first valley
            tmpIdx = int(bottomIdxList[0])
        else:        # get last valley
            tmpIdx = int(bottomIdxList[-1])     #print(tmpIdx)    #print(indexList[tmpIdx])
        # calc peaks beside the curve bottom
        leftPeak, rightPeak = anaToolCurveFindPeaksNearValley.find_peaks_around_specValley_scipy(tmpIdx, filterOutYarray, self.peakThreshold)
        # get proper curve positions according to request
        if   self.returnPoint=="start": # return the left peak
            if leftPeak is None:            return ( indexList[tmpIdx] + self.fixFrameNumber )
            else:            return ( indexList[leftPeak] + self.fixFrameNumber )
        elif self.returnPoint=="stop": # return the right peak
            if rightPeak is None:                return ( indexList[tmpIdx] + self.fixFrameNumber )
            else:                return ( indexList[rightPeak] + self.fixFrameNumber )
        elif self.returnPoint=="startAtMid":
            if debug_level > 1:
                print(f"bottom_index={indexList[tmpIdx]}, left_peak_index={indexList[leftPeak]}, right_peak_index={indexList[rightPeak]}")
            if leftPeak is None:            return ( indexList[tmpIdx] + self.fixFrameNumber )
            else:            return ( int((indexList[leftPeak]+indexList[tmpIdx])/2) + self.fixFrameNumber )
        elif self.returnPoint=="stopAtMid":
            if debug_level > 1:
                print(f"bottom_index={indexList[tmpIdx]}, left_peak_index={indexList[leftPeak]}, right_peak_index={indexList[rightPeak]}")
            if rightPeak is None:            return ( indexList[tmpIdx] + self.fixFrameNumber )
            else:            return ( int((indexList[rightPeak]+indexList[tmpIdx])/2) + self.fixFrameNumber )
        else:
            return ( indexList[tmpIdx] + self.fixFrameNumber )
        return -1
