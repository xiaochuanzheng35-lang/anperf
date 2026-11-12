import cv2
import numpy as np
from . import anPerfToolFrameProc, anPerfToolDebug

# 常量定义
FEATURE_METHOD = "SIFT"  # 使用的特征检测算法
g_detector = None  # 特征检测器实例

def calc_match_ratio(prev_roi, curr_roi, debug_level=0):
    global g_detector
    if g_detector is None:
        g_detector = cv2.SIFT_create()

    # 转换为灰度图
    prev_gray = cv2.cvtColor(prev_roi, cv2.COLOR_BGR2GRAY) if len(prev_roi.shape) == 3 else prev_roi
    curr_gray = cv2.cvtColor(curr_roi, cv2.COLOR_BGR2GRAY) if len(curr_roi.shape) == 3 else curr_roi

    # 提取特征点和描述符
    kp1, des1 = g_detector.detectAndCompute(prev_gray, None)
    kp2, des2 = g_detector.detectAndCompute(curr_gray, None)

    if des1 is None or des2 is None or len(kp1) < 2 or len(kp2) < 2:
        #print("Failed to extract SIFT data from frame! Set match ratio to max 0.99" )        #print(f"无法提取足够特征点")
        #return 0.01
        return 0.99

    # 使用FLANN匹配器
    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)

    matches = flann.knnMatch(des1, des2, k=2)
    good_matches = [m for m, n in matches if m.distance < 0.7 * n.distance]

    match_ratio = len(good_matches) / min(len(kp1), len(kp2)) if min(len(kp1), len(kp2)) > 0 else 0.0
    #avg_distance = np.mean( [m.distance for m in good_matches] )
    #match_ratio  = 1 / (1+avg_distance) 

    anPerfToolDebug.showCvImage(debug_level, curr_roi, 0)
    # 显示匹配结果
    if debug_level>2:
        print(f"Frame2Frame match ratio = {match_ratio:.3f}")
        match_img = cv2.drawMatches(prev_roi, kp1, curr_roi, kp2, good_matches, None,
                                    flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
        cv2.imshow('Feature Matching Result', match_img)
        cv2.waitKey(1)

    return match_ratio
