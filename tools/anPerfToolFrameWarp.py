import os, sys, cv2
import numpy as np

def order_points(pts):
    # Initialise a list of coordinates that will be ordered
    # (top-left, top-right, bottom-right, bottom-left)
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]  # Top-left has smallest sum
    rect[2] = pts[np.argmax(s)]  # Bottom-right has largest sum
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)] # Top-right has smallest difference
    rect[3] = pts[np.argmax(diff)] # Bottom-left has largest difference
    return rect

def proc(img, contour_pts):
    rect = order_points(contour_pts.reshape(4, 2))
    (tl, tr, br, bl) = rect

    # Compute width and height of the new image
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))

    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))

    # Destination points for a flat rectangle
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")

    M = cv2.getPerspectiveTransform(rect, dst)
    return cv2.warpPerspective(img, M, (maxWidth, maxHeight))



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
