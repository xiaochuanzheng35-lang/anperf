import cv2

def getFrameList(input_path):
    cap = cv2.VideoCapture(input_path)
    retFrameList = []
    while 1:
        ret, frame = cap.read()
        if not ret:
            break
        retFrameList.append(frame)
    return retFrameList

def frames_to_video(frame_list, output_path, fps):
    if not frame_list:
        print("Error: The frame list is empty.")
        return

    # Determine size from the first frame in the list
    height, width, layers = frame_list[0].shape
    size = (width, height)

    # Set up the writer (mp4v is a standard codec for .mp4)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, int(fps), size)

    for frame in frame_list:
        # Note: OpenCV expects BGR format
        out.write(frame)

    out.release()
    print(f"Video successfully saved to {output_path}")


# Example Usage:
# dump_video_part("input.mp4", "output_clip.mp4", 10, 20, 30)