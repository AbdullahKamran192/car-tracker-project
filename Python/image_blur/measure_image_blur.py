import cv2
import numpy as np
import os

def measureImageBlur(array_of_plates_images):

    for plate_image in array_of_plates_images:
        laplacian = cv2.Laplacian(plate_image, cv2.COLOR_BGR2GRAY).var() # high value = sharp image , low value = blurry image
        print(F"PLATE BLUR VALUE: {laplacian}")

        if laplacian < 5:
            array_of_plates_images.remove(plate_image)
            print("PLATE TOO BLURRY, REMOVED")

    # for plate in os.listdir("Python/plates"):
    #     plate_path = os.path.join('Python/plates', plate)
    #     img_of_plate = cv2.imread(plate_path)

    #     laplacian = cv2.Laplacian(img_of_plate, cv2.COLOR_BGR2GRAY).var() # high value = sharp image , low value = blurry image
    #     print(F"PLATE BLUR VALUE: {laplacian}")

    #     if laplacian < 5:
    #         os.remove(plate_path)
    #         print("PLATE TOO BLURRY, DELETED")
    
    #return laplacian

