"""
视频时间计算工具集
"""
def calculate_frame_interval_duration(perfstart_frame_index, perfend_frame_index, fps=240):
    frameGapNum = (perfend_frame_index - perfstart_frame_index)
    sec = int( frameGapNum/fps )
    ms = round(1000*(frameGapNum%fps)/fps)
    #return str(sec)+"s "+str(ms)+"ms"
    str_ms = "%03d" % ms
    return str(sec)+"."+str_ms

def frames_to_timecode(frames, fps=240, show_frames=False):
    sec = int( frames/fps )
    ms = round(1000*(frames%fps)/fps)
    #return str(sec)+"s "+str(ms)+"ms"
    str_ms = "%03d" % ms
    return str(sec)+"."+str_ms

def printAnPerfResults(perfstart_frame_index, perfend_frame_index, fps=240):
    print("===== find start and end frame :")
    print(perfstart_frame_index)
    print(perfend_frame_index)
    time_str = calculate_frame_interval_duration(perfstart_frame_index, perfend_frame_index, fps)
    start_time_str = frames_to_timecode(perfstart_frame_index, fps)
    stop_time_str = frames_to_timecode(perfend_frame_index, fps)
#    print(f"时长: {time_str}")
#    print(f"起始: {frames_to_timecode(perfstart_frame_index)}")
#    print(f"结束: {frames_to_timecode(perfend_frame_index)}")
    #print("时长: " + time_str + ", " + "起始: " + start_time_str + ", " + "结束: " + stop_time_str)
    perftimeDataList = [time_str, start_time_str, stop_time_str]
    print(perftimeDataList)
    return perftimeDataList

if __name__ == "__main__":
    printAnPerfResults(2299, 7740, 120)
#    printAnPerfResults(1070, 1414)
