import os
import cv2
import random
import string

from detect_number_plates.predict_write_images import detect_number_plate_method
from read_text_programs.read_image_car_plate import detect_number_plate_text
from openai_api.openai_api_read_image_text import openai_read_image
import database.mysql_database as database
from dvla_api.dvla_api_get_car_info import get_car_info
from aws.s3.s3_store_number_plate import upload_current_frame_to_s3
from image_blur.measure_image_blur import measureImageBlur
from frame_resolution.number_plate_resolution import checkNumberPlateResolution


VIDEOS_DIR = os.path.join('.', 'Python', 'videos')
video_path = os.path.join(VIDEOS_DIR, 'cars2.mp4')

cap = cv2.VideoCapture(video_path)
ret, frame = cap.read()

count = 0
frame_counter = 1
frame_read = 60 #read every 60th frame
image_clarity_percentage_threshold = 0.19 # How high resolution the number plate image should be. Percentage out of 100.
laplacian_threshold = 5 # How clear/sharp an image should be

while ret:
    if frame_counter % frame_read == 0:
        frame_counter += 1
        frame = cv2.resize(frame, (1920, 1080))

        for file in os.listdir("Python/current_frame"):
            if os.path.exists(f'Python/current_frame/{file}'):
                os.remove(f'Python/current_frame/{file}')

        cv2.imwrite('Python/current_frame/current_frame.jpg', frame)

        cv2.imshow("frame", frame)
        cv2.waitKey(1)

        array_of_plates_images = []

        # 1.  call the detect_number_plates program. Which detects number plates and stores them in the Python/plates folder.
        array_of_plates_images = detect_number_plate_method(frame, array_of_plates_images)

        # Calculate the resolution of the number plate image divide by the frame. If percentage it's below a threshold, the number plate image is blurry, too far, delete it.

        array_of_plates_images = checkNumberPlateResolution(frame, array_of_plates_images)
        
        # Check the image is not too blurry. laplacian value should be above the threshold

        array_of_plates_images = measureImageBlur(array_of_plates_images)

        # 2. check if each image in Python/plates contains text. if it doesn't contain text, delete that plate file.

        array_of_plates_images = detect_number_plate_text(array_of_plates_images)
        
        # 3. The similarity checker. if it contains plate text similar to ones already present. delete file/image.


        # 4a OpenAI API

        print("============= AI turn now ===========")

        array_of_plates_text = openai_read_image(array_of_plates_images)

        #5. if the plate OpenAI read already exist on database for today. Remove

        for plate_text in array_of_plates_text:
            print(f"Plate to be received from database: {plate_text.upper()}")
            check_plate_on_database = database.getCar(plate_text.upper())
            print(f"Plate received on database: {check_plate_on_database}")

            if check_plate_on_database:
                array_of_plates_text.remove(plate_text)
        
        #6. get data from DVLA

        array_of_cars_info = []

        for plate_text in array_of_plates_text:
            array_of_cars_info.append(get_car_info(plate_text.upper()))

        #7. Store image to AWS

        if array_of_cars_info:
            length = 16
            random_file_name = ''.join(random.choices(string.ascii_letters + string.digits, k=length))

            file_name = f'{random_file_name}.jpg'

            upload_current_frame_to_s3("Python/current_frame/current_frame.jpg",file_name)

        #8. Store car info on the datbase

            for car_info in array_of_cars_info:
                print(f"Storing to database: {car_info["registrationNumber"]}, {car_info["make"]}, {car_info["colour"]}")
                database.insertCar(car_info["registrationNumber"], car_info["make"], car_info["colour"], random_file_name)

        array_of_plates_images.clear()
        array_of_cars_info.clear()
        array_of_plates_text.clear()

        # 8. Clear the plates folder

        for file in os.listdir("Python/plates"):
            if os.path.exists(f'Python/plates/{file}'):
                os.remove(f'Python/plates/{file}')

    else:
        frame_counter += 1
    
    ret, frame = cap.read()

cap.release()
cv2.destroyAllWindows()