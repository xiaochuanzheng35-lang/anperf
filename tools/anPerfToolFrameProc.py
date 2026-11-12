import os, sys, cv2

def crop(single_frame_data, heightStartPercent, heightEndPercent, widthStartPercent, widthEndPercent):
    debug_mode = False #True
    # 裁剪帧
    frame_height, frame_width = single_frame_data.shape[:2]
    cropped_frame = single_frame_data[
                    int(frame_height * heightStartPercent):int(frame_height * heightEndPercent),
                    int(frame_width * widthStartPercent):int(frame_width * widthEndPercent)
                    ]
    if debug_mode:
        cv2.imshow('Processed Frame', cropped_frame) # 显示处理后的帧，当用户按下q键时，退出循环
        if cv2.waitKey(1) & 0xFF == ord('q'):
            return -1
    return cropped_frame

def cropAndDenoise(single_frame_data, heightStartPercent, heightEndPercent, widthStartPercent, widthEndPercent):
    cropped_frame = crop(single_frame_data, heightStartPercent, heightEndPercent, widthStartPercent, widthEndPercent)
    denoised_frame = cv2.blur(cropped_frame, (5,5))    #denoised_frame = cv2.GaussianBlur(denoised_frame, (5,5), 0)
    return denoised_frame

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python script.py <视频文件路径>")
        sys.exit(1)
    cap = cv2.VideoCapture( sys.argv[1] )
    if not cap.isOpened():
        print(f"无法打开视频文件 {sys.argv[1]}")
        sys.exit(1)
    while True:
        ret, frame = cap.read()  # 读取视频帧
        if not ret:  # 检查是否读取成功
            break
        cropped_frame = crop( frame, 0.625, 0.725, 0.15, 0.32 )
        ret = input()
        if 'e' in ret:
            break
    cap.release()
    cv2.destroyAllWindows()
