import cv2
from . import anPerfToolCvSSIMmatcher, anPerfToolDebug


def proc(compFrameLst, startFrmIdx, stepFrmNum, debug_level):
    score_list = []
    index_list = []
    # start computing
    tmp_gray = cv2.cvtColor(compFrameLst[0], cv2.COLOR_BGR2GRAY)
    prev_gray = cv2.GaussianBlur(tmp_gray, (5, 5), 0)
    for i in range(1, len(compFrameLst)):
        curr_gray = cv2.cvtColor(compFrameLst[i], cv2.COLOR_BGR2GRAY)
        score = anPerfToolCvSSIMmatcher.calc_match_score(prev_gray, curr_gray, debug_level)
        score_list.append(score)
        frameIndex = (startFrmIdx + i * (stepFrmNum+1))
        index_list.append(frameIndex)
        if debug_level>2:
            print(f"frameIndex={frameIndex}, score={score}")
        anPerfToolDebug.showCvImage(debug_level, curr_gray, frameIndex)
        prev_gray = cv2.GaussianBlur(curr_gray, (5, 5), 0)
    return (index_list, score_list)
