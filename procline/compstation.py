import os, cv2
from . import perfAnaCommon
from tools import anPerfToolFrameProc, anPerfToolDebug, VideoTools

def procVideo(pointIndex, videoCap, startIdx, stepNum, stopIdx, procWay, procMethodObj, preprocMethodObjList, areaRectLst):
    compFrameLst,frameIdxList = _loadallprocFrameList(pointIndex, videoCap, startIdx, stepNum, stopIdx, procMethodObj, preprocMethodObjList, areaRectLst)
    if "reverse"==procWay:
        compFrameLst.reverse()
        frameIdxList.reverse()
    ret = procMethodObj.proc(compFrameLst, frameIdxList, perfAnaCommon.g_debug_level)
    anPerfToolDebug.printDataAndWaitForInput( perfAnaCommon.g_debug_level, ret, "Find frame index = " )
    return ret

def loadCoreProcMethod(cmpStationConfDict):    #coreprocMethodObj = None
    preprocMethodObjLst = [] # [ preprocMethod1, preprocMethod2, preprocMethod3, ... ]
    computeMethod  = cmpStationConfDict["findFrameMethod"]
    print(f"Compute method = {computeMethod}")
    methodConfDict = {}
    if "methodConfig" in cmpStationConfDict.keys():        methodConfDict = cmpStationConfDict[ "methodConfig" ]
    print(methodConfDict)
    coreprocMethodObj = perfAnaCommon.getClassObj("method4proc", computeMethod)
    if coreprocMethodObj is None:
        print(f"Error: failed to load core process method -- {computeMethod}")
    else:
        if 0!=coreprocMethodObj.init(methodConfDict):
            print(f"Error: failed to init load config for core process method -- {computeMethod}")
        else:
            if "preprocMethod" in methodConfDict.keys():
                preprocMethodObj = perfAnaCommon.selectPreProcMethod( methodConfDict["preprocMethod"] )
                if preprocMethodObj is not None:
                    preprocMethodObjLst.append(preprocMethodObj)
            elif "preprocMethodList" in methodConfDict.keys():
                preprocMethodObjLst = perfAnaCommon.selectPreProcMethodList( methodConfDict["preprocMethodList"] )
    return preprocMethodObjLst, coreprocMethodObj

def _stepFrames(videoCap, stepFrmNum, currFrameIndex):    # step over some frames if needed
    if stepFrmNum>0:
        for i in range(0, stepFrmNum):            videoCap.grab()
    return (currFrameIndex+stepFrmNum)

def _preprocFrame(frame, areaRectLst, preprocMethodObjList):
    procframe = anPerfToolFrameProc.crop(frame,areaRectLst[0],areaRectLst[1],areaRectLst[2],areaRectLst[3]) # crop frame to reduce size
    for preprocObj in preprocMethodObjList:        procframe = preprocObj.proc(procframe, perfAnaCommon.g_debug_level)
    return procframe

def _getCacheVideoPartFile(pointIndex, startIdx, stepNum, stopIdx):
    return os.path.join( perfAnaCommon.debugWorkPath, f"{pointIndex}_{startIdx}_{stepNum}_{stopIdx}.mp4" )

def _loadallprocFrameList(pointIndex, videoCap, startIdx, stepNum, stopIdx, procMethodObj, preprocMethodObjList, areaRectLst):
    if len(perfAnaCommon.debugWorkPath)>0:
        cacheVideoFile = _getCacheVideoPartFile(pointIndex, startIdx, stepNum, stopIdx)
        if os.path.isfile( cacheVideoFile ):
            compFrameLst = VideoTools.getFrameList(cacheVideoFile)
            frameIdxList = []
            for i in range(0, len(compFrameLst)):
                frameIdxList.append( startIdx + i*(stepNum+1) )
            return compFrameLst,frameIdxList
    ### 1. read frame list out of video
    compFrameLst = []
    frameIdxList = []
    procframeIdx = startIdx - 1
    videoCap.set( cv2.CAP_PROP_POS_FRAMES, max(0,startIdx) )
    while procframeIdx<=stopIdx:
        ret, frame = videoCap.read()
        if not ret:            break
        procframeIdx += 1
        frame = perfAnaCommon.preproc(frame)
        compFrameLst.append( _preprocFrame(frame, areaRectLst, preprocMethodObjList) )
        frameIdxList.append( procframeIdx )
        procframeIdx = _stepFrames(videoCap, stepNum, procframeIdx)
    if len(perfAnaCommon.debugWorkPath)>0:
        cacheVideoFile = _getCacheVideoPartFile(pointIndex, startIdx, stepNum, stopIdx)
        VideoTools.frames_to_video(compFrameLst, cacheVideoFile, perfAnaCommon.videoFPS)
    return compFrameLst,frameIdxList
