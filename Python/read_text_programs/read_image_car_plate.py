import sys
import cv2
import numpy as np
import easyocr
import matplotlib.pyplot as plt
import time
import os


def read_adjusted_image_method(img, thresh_value=100):

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imshow("Gray Plate", gray)

    # Average brightness (0–255)
    brightness = int(gray.mean())
    print("Brightness (0-255):", brightness)

    # As percentage
    #brightness_percent = (brightness / 255)
    #print("Brightness (%):", brightness_percent)

    #thresh_value = int((brightness - (brightness * brightness_percent)))
    #print(f"trash value: {thresh_value}")

    ret, thresh = cv2.threshold(gray, thresh_value, 255, cv2.THRESH_BINARY)
    cv2.imshow("threshold Plate", thresh)

    # thresh is your binary image
    h, w = thresh.shape
    black_mask = (thresh == 0).astype(np.uint8) * 255

    # find connected black areas
    num, labels, stats, _ = cv2.connectedComponentsWithStats(black_mask, connectivity=8)

    result = thresh.copy()

    for i in range(1, num):  # skip background
        x, y, bw, bh, area = stats[i]
        if area > 0.05 * h * w or bw > 0.6 * w or bh > 0.6 * h:  # large blob
            result[labels == i] = 255   # paint white

    cv2.imshow("Cleaned", result)

    #==================== IMAGE TEXT READER ====================
    img = result

    # instance text detector
    reader = easyocr.Reader(['en'], gpu=False)

    # detect text on image
    text_ = reader.readtext(img)

    threshold = 0.05
    # draw bbox and text
    for t_, t in enumerate(text_):
        #print(t)

        bbox, text, score = t

        if score > threshold:
            cv2.rectangle(img, bbox[0], bbox[2], (0, 255, 0), 5)
            cv2.putText(img, text, bbox[0], cv2.FONT_HERSHEY_COMPLEX, 0.65, (255, 0, 0), 2)

            #print(f"The text was {text.upper()}")

            #plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            #plt.show()

            return text

    #plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    #plt.show()

    #cv2.waitKey(0)

    return ""


#detect_number_plate_text() checks if an image contains text and returns TRUE or FALSE.
def detect_number_plate_text(frame):
    
    try:
        plate_text = read_adjusted_image_method(frame)
    except Exception:
        print("Something went wrong")
    
    if plate_text and len(plate_text) > 0:
        return True
    else:
        return False