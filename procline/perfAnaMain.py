import cv2
from . import compline, calcBeginEndFrameIndex, perfAnaCommon
from tools import anPerfToolCalcFrameTime

def videoAnalyze(videoFile, caseConfigDict):
    videoCap = cv2.VideoCapture( videoFile )
    if not videoCap.isOpened():
        print(f"Error: failed to open {videoFile}")
        return {}
    ### 2. start main process
    findFrameIdxList = compline.setline2Compute( videoCap, caseConfigDict )
    videoCap.release()
    cv2.destroyAllWindows()
    ### 3. calc time stamps by frame index
    if len(findFrameIdxList)<2:
        return {}
    print("\n>>>>> all compute frame indexs here >>>>> ")
    print(findFrameIdxList)    #print("\n\n")
    timeConfigDict = caseConfigDict["compBeginEndTimeConfDict"]
    foundFrameIdxLst = calcBeginEndFrameIndex.selectFromFrameIndexList(findFrameIdxList, timeConfigDict)    #print(tmplst)
    if 0==len(foundFrameIdxLst): # at least 2 frame index to calculate start and end time stamp
        return {}
    perftimeList = anPerfToolCalcFrameTime.printAnPerfResults(foundFrameIdxLst[0], foundFrameIdxLst[1], perfAnaCommon.videoFPS)        #print(perftimeList)
    return {
        "perftime"      :    perftimeList[0],
        "timeStampLst"  :    [ perftimeList[1], perftimeList[2] ],
        "frameIdxList"  :    foundFrameIdxLst
    }

# the following method failed to get accurate time in high FPS video
def _getTimeMsInVideoByFrameIndex(videoCap, frameIndex):
    videoCap.set(cv2.CAP_PROP_POS_FRAMES, frameIndex)
    # Retrieve timestamp in milliseconds in the video
    return videoCap.get(cv2.CAP_PROP_POS_MSEC)

def _formatFloat2String(floatValue):
    return f"{floatValue:.3f}"
