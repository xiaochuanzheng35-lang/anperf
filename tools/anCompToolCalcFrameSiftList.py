import cv2
from . import anPerfToolCvSIFTmatcher


def proc(compFrameLst, startFrmIdx, stepFrmNum, debug_level):
    frameSiftBottomLimit = 0.02 #0.2
    cmpSiftFrmLst = []
    indexList = []
    ratioList = []
    cmpSiftFrmLst.append( compFrameLst[0] )
    cmpFrmIdxInVideo = startFrmIdx
    for compFrmIdxInLst in range(1, len(compFrameLst)):
        cmpSiftFrmLst.append( compFrameLst[compFrmIdxInLst] )
        cmpFrmIdxInVideo += (1 + compFrmIdxInLst * stepFrmNum)
        indexList.append( cmpFrmIdxInVideo )
        # calc sift of 2 frames
        match_ratio = anPerfToolCvSIFTmatcher.calc_match_ratio(cmpSiftFrmLst[0], cmpSiftFrmLst[1], debug_level)
        if match_ratio>frameSiftBottomLimit:
            ratioList.append( match_ratio )
        else:
            ratioList.append( frameSiftBottomLimit )
        cmpSiftFrmLst.pop(0)
    if debug_level>2:
        for i in range(0, len(indexList)):
            print(f"{indexList[i]} -- {ratioList[i]:.3f}")
    return (indexList, ratioList)

def proc1(compFrameLst, frameIdxList, debug_level):
    frameSiftBottomLimit = 0.02 #0.2
    indexList = []
    ratioList = []
    last_frame = compFrameLst[0]
    for i in range(1, len(compFrameLst)):
        curr_frame = compFrameLst[i]
        indexList.append( frameIdxList[i] )
        # calc sift of 2 frames
        match_ratio = anPerfToolCvSIFTmatcher.calc_match_ratio(last_frame, curr_frame, debug_level)
        ratioList.append( max(match_ratio, frameSiftBottomLimit) )
        last_frame = curr_frame
    if debug_level>3:
        for i in range(0, len(indexList)):
            print(f"{indexList[i]} -- {ratioList[i]:.3f}")
    return (indexList, ratioList)
