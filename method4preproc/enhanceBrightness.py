import os, cv2
from tools import anPerfToolDebug

class enhanceBrightness(object):

    def proc(self, procframe, debug_level):
        # 2. Convert to LAB color space (L=Lightness, A/B=Color channels)
        lab = cv2.cvtColor(procframe, cv2.COLOR_BGR2LAB)
        l_channel, a, b = cv2.split(lab)
    
        # 3. Apply CLAHE to the L-channel
        # clipLimit: higher = more contrast; tileGridSize: smaller = more local detail
        clahe = cv2.createCLAHE(clipLimit=3.5, tileGridSize=(8,8))
        cl = clahe.apply(l_channel)
    
        # 4. Merge back and convert to BGR
        limg = cv2.merge((cl, a, b))
        enhanced_img = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

        anPerfToolDebug.showCvImage(debug_level, enhanced_img, 0)

        return enhanced_img
