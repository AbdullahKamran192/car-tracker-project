import cv2
import numpy as np

def measureImageBlur(frame):
    laplacian = cv2.Laplacian(frame, cv2.COLOR_BGR2GRAY).var() # high value = sharp image , low value = blurry image
    return laplacian

