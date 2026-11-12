from . import anPerfToolDebug
import cv2
import numpy as np
# Remember: pip install scikit-image
from skimage.metrics import structural_similarity as ssim

def calc_match_score(prev_gray, current_gray, debug_level=0):
    # Alignment settings to counter camera sway
    warp_mode = cv2.MOTION_TRANSLATION
    warp_matrix = np.eye(2, 3, dtype=np.float32)
    criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 50, 0.001)
    h, w = prev_gray.shape[:2]
    #current_gray = cv2.cvtColor(procframe, cv2.COLOR_BGR2GRAY)
    # 1. Align the frame to fix camera sway
    try:
        _, warp_matrix = cv2.findTransformECC(
            prev_gray, current_gray, warp_matrix, warp_mode, criteria, inputMask=None, gaussFiltSize=1
        )
        aligned_gray = cv2.warpAffine(
            current_gray, warp_matrix, (w, h), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP
        )
    except cv2.error:
        # If tracking drops for a split second, fall back to the unaligned frame
        aligned_gray = current_gray
    # 2. Smooth out high-frequency camera noise
    blurred_gray = cv2.GaussianBlur(aligned_gray, (5, 5), 0)
    # 3. Structural Comparison (Using correct variables)
    # score ranges from -1 (completely different) to 1 (perfect match)
    score, diff_image = ssim(prev_gray, blurred_gray, full=True)
    if debug_level>3:
        anPerfToolDebug.showCvImage(debug_level, diff_image, 0)
    return score
