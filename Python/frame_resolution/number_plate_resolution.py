import os
import cv2

image_clarity_percentage_threshold = 0.19 # How high resolution the number plate image should be. Percentage out of 100.

def checkNumberPlateResolution(frame):
    frame_height, frame_width, channels = frame.shape

    for plate in os.listdir("Python/plates"):
        plate_path = os.path.join('Python/plates', plate)
        img_of_plate = cv2.imread(plate_path)

        plate_height, plate_width, channels = img_of_plate.shape

        image_clarity_percentage = ((plate_height * plate_width) / (frame_height * frame_width)) * 100

        if image_clarity_percentage < image_clarity_percentage_threshold:
            os.remove(plate_path)
            print("PLATE RESOLUTION TOO LOW, DELETED.")