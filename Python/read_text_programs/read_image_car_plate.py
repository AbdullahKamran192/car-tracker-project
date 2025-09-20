import sys
import cv2
import numpy as np
import easyocr
import matplotlib.pyplot as plt
import time
import os


#print("Welcome to ", str(sys.argv))

#sentence = 'Welcome to ' + str(sys.argv)

correct_plates_text = {
    "plate1": "RV59 VRO",
    "plate2": "LY66 FCO",
    "plate3": "EK67 XUL",
    "plate4": "EY66 ZXC",
    "plate5": "JCC 3P",
    "plate6": "ND66 YEJ",
    "plate7": "KY68 WZM",
    "plate8": "LB02 APF",
    "plate9": "BN65 GTU",
    "plate10": "SJ10 HLR",
    "plate11": "MY 2 OHMS", # remove this plate, no one really knows if its 0 or O
    "plate12": "NO67 GAS"
}

car_plates_read = []

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


    #===========================================================

    #cv2.waitKey(0)



#test one image
def test_image(filename):

    image_path = f'./plates2/{filename}.jpg'
    img = cv2.imread(image_path)

    plate_text = read_adjusted_image_method(img)

    print(f"The {filename} is {plate_text.upper()}.")

    plate_text = plate_text.upper()

    if plate_text == correct_plates_text.get(filename):
        print(f"{plate_text} was read correctly")

#test_image('scanned_img_102')




#tests multiple images in one go. for example test read every image in the plates2 folder.
def test_images_method2():

    correct_plates_read_count = 0

    for i in range(1,12):
        plate = f"plate{i}"
        image_path = f'data/{plate}.jpg'
        img = cv2.imread(image_path)

        for thresh_value in range(0, 255, 10):

            plate_text = read_adjusted_image_method(img, thresh_value=thresh_value)

            print(f"The {plate} is {plate_text.upper()}.")

            plate_text = plate_text.upper()

            if plate_text == correct_plates_text.get(plate):
                print(f"{plate_text} was read correctly")
                correct_plates_read_count += 1
                break

def count_files_with_text_detected_method():

    count_files_with_text_detected = 0

    for i in range(1, 200):
        img_name = f'scanned_img_{i}.jpg'
        image_path = f'./plates2/{img_name}'
        img = cv2.imread(image_path)

        print(f'The value of i is {i}')

        try:
            plate_text = read_adjusted_image_method(img)
        except Exception:
            print("Something went wrong")
            continue
        print(f"The {image_path} is {plate_text.upper()}.")

        #plate_text = plate_text.upper()

        if len(plate_text) > 0:
            count_files_with_text_detected += 1
            #move that file
            destination = f'./images_with_text/{img_name}'

            if os.path.exists(destination):
                print("There is already a file there")
            else:
                os.replace(image_path, destination)
                

    
    print(f'{count_files_with_text_detected} FILES WERE READ!!!!')

count_files_with_text_detected_method()

#test reading the images on different thresh values makes it more like that an image is read.
#It does take more computing power and time, but if you are interested, you can use it.
def test_image_threshes(filename):
    image_path = f'data/{filename}.jpg'
    img = cv2.imread(image_path)

    for thresh_value in range(0, 255, 10):
        plate_text = read_adjusted_image_method(img, thresh_value=thresh_value)

        print(f"The {filename} is {plate_text.upper()}.")

        plate_text = plate_text.upper()

        if plate_text == correct_plates_text.get(filename):
            print(f"{plate_text} was read correctly")
            break

#sys.stdout.flush()