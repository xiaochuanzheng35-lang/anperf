import os, cv2, sys

def extract_text_from_frame(frame_data):
    """从帧数据中提取所有文本并合并为字符串"""
    return "".join([item['text'] for item in frame_data])

def calculate_match_score(text, keywords):
    """计算文本与关键词列表的匹配分数"""
    #matched_chars = set()
    #for keyword in keywords:
    #    for char in keyword:
    #        if char in text:
    #            matched_chars.add(char)
    #return len(matched_chars) / sum(len(keyword) for keyword in keywords)
    sum = 0
    for keyword in keywords:
        if keyword in text:
            sum += 1
    return sum/len(keywords)

def find_match_frame(frame_detect_result, refer_keywords, threshold=0.53):
    """查找匹配的帧"""
    frame_text = extract_text_from_frame(frame_detect_result)
    score = calculate_match_score(frame_text, refer_keywords)
    # print info in debug_mode
    #print(frame_text)
    #print(refer_keywords)
    #print(score)
    if score >= threshold:
        return True
    return False
