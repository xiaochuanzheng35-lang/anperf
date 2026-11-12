import cv2
from . import compstation, perfAnaCommon

def setline2Compute(videoCap, caseConfigDict):
    # NOTE: the following method is not always precise -- TODO: use FFmepg to get
    totalFrameNum = int( videoCap.get(cv2.CAP_PROP_FRAME_COUNT) )    #print(f"video frames = {totalFrameNum}")
    ### 1. load compute station list and start
    compStationConfList  = caseConfigDict["compStationConfigList"]
    findFrameIndexList = []
    ### 2. start the loop to execute each compute station
    for i in range(0, len(compStationConfList)):
        print(f"\n+++++ {(i)} key point to compute")
        # skip if in debug mode and frame index of this key point already computed
        if len(perfAnaCommon.debugWorkPath)>0 and len(perfAnaCommon.debugFrameIndexList)>i and perfAnaCommon.debugFrameIndexList[i]>0:
            retFrameIndex = perfAnaCommon.debugFrameIndexList[i]
        else: # do frame-by-frame computing here
            compStaConfigDict = compStationConfList[i]        #print(compStaConfigDict)
            procWay = _getProcWay(compStaConfigDict)
            [startFrmIdx, stepFrmNum, stopFrmIdx] = _getFrameParams(compStaConfigDict, findFrameIndexList, totalFrameNum-1)
            if startFrmIdx<0:            break
            ## get process method and preproc method
            preprocObjList, procObj = compstation.loadCoreProcMethod(compStaConfigDict)
            if procObj is None:
                print("Error: failed to get process method.")
                break
            # input all data and methods, start video processing
            retFrameIndex = compstation.procVideo(i, videoCap, startFrmIdx, stepFrmNum, stopFrmIdx, procWay, procObj,preprocObjList, compStaConfigDict["areaRectSpecified"])
        # append computed frame index #if retFrameIndex>0:
        findFrameIndexList.append(retFrameIndex)
        print(f"----- {(i)} key point compute done: Find frame index = {retFrameIndex}")
        # append data to debug frame index list
        if len(perfAnaCommon.debugWorkPath)>0:
            if len(perfAnaCommon.debugFrameIndexList)>i:
                perfAnaCommon.debugFrameIndexList[i] = retFrameIndex
            else:
                perfAnaCommon.debugFrameIndexList.append(retFrameIndex)
    if len(findFrameIndexList)==len(compStationConfList):
        return findFrameIndexList
    return []

def _getFrameParams(compStaConfigDict, findFrameIndexList, videoMaxFrameIdx):
    [startFrmIdx, skipFrameNum, stepFrmNum, maxCompFrameNum] = compStaConfigDict["computeFrameData"]
    if  startFrmIdx<0:
        startFrmIdx = findFrameIndexList[ startFrmIdx ]
    return [ (startFrmIdx+skipFrameNum), stepFrmNum, (startFrmIdx+maxCompFrameNum) ]

def _getProcWay(compStaConfigDict):
    if "videoProcWay" in compStaConfigDict.keys():
        return compStaConfigDict["videoProcWay"]
    return "forward"
