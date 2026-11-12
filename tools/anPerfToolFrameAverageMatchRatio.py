import os, cv2
from . import anPerfToolCvSIFTmatcher, anPerfToolDebug

g_prev_cropped_frame = None
g_monit_window_length = 20
g_monit_window_list = []

def calc_average_match_ratio(cropped_frame, frame_index):
    global g_prev_cropped_frame, g_monit_window_length, g_monit_window_list
    debug_mode = False #True #

    if g_prev_cropped_frame is None:
        g_prev_cropped_frame = cropped_frame
        return 0

    match_ratio = anPerfToolCvSIFTmatcher.calc_match_ratio(g_prev_cropped_frame, cropped_frame)

    g_prev_cropped_frame = cropped_frame
    # update monitor list
    g_monit_window_list.append(match_ratio)
    if len(g_monit_window_list)<=g_monit_window_length:
        return 0
    g_monit_window_list.pop(0)

    # 计算监测窗口中的相似度均值
    change_trend = sum(g_monit_window_list)/len(g_monit_window_list)
    anPerfToolDebug.printData( debug_mode, frame_index, "frame index =" )
    anPerfToolDebug.printData( debug_mode, change_trend, "average-frame-match-ratio =" )
    return change_trend

def init(monit_window_length):
    global g_prev_cropped_frame, g_monit_window_length, g_monit_window_list
    g_prev_cropped_frame = None
    g_monit_window_length = monit_window_length
    g_monit_window_list = []
