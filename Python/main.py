import os
import cv2
import time
import random
import string
import boto3

from detect_number_plates.predict_write_images import detect_number_plate_method
from read_text_programs.read_image_car_plate import detect_number_plate_text
from openai_api.openai_api_read_image_text import openai_read_image
import database.mysql_database as database
from dvla_api.dvla_api_get_car_info import get_car_info


s3 = boto3.client('s3')
bucket_name = 'test-bucket-123pdf123'


VIDEOS_DIR = os.path.join('.', 'Python', 'videos')
video_path = os.path.join(VIDEOS_DIR, 'cars2.mp4')

cap = cv2.VideoCapture(video_path)
ret, frame = cap.read()

count = 0
frame_counter = 1
frame_read = 20 #read every 20th frame

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

        # 1.  call the detect_number_plates program. Which detects number plates and stores them in the Python/plates folder.
        detect_number_plate_method(frame)

        # 2. check if each image in Python/plates contains text. if it doesn't contain text, delete that plate file.

        for plate in os.listdir("Python/plates"):
            plate_path = os.path.join('Python/plates', plate)
            img_of_plate = cv2.imread(plate_path)

            if detect_number_plate_text(img_of_plate) is False:
                #False. text hasn't been detected.
                os.remove(plate_path)
                print("PLATE HAS BEEN DELETED!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            

        
        # 3. The similarity checker. if it contains plate text similar to ones already present. delete file/image.


        # 4a. OpenAI API

        print("============= AI turn now ===========")

        for plate in os.listdir("Python/plates"):
            plate_path = os.path.join('Python/plates', plate)

            plate_text = openai_read_image(plate_path)
            plate_text = plate_text.replace(' ', '')

            print(f"OpenAI read {plate_path} as: {plate_text.upper()}")

            # 4b. if the plate OpenAI read already exist on database for today. ignore

            print(f"Plate to be received from database: {plate_text.upper()}")
            check_plate_on_database = database.getCar(plate_text.upper())
            print(f"Plate received on database: {check_plate_on_database}")

            if check_plate_on_database:
                os.remove(plate_path)
            else:
                #5. get data from DVLA.
                car_info = get_car_info(plate_text.upper())

                if car_info:
                    #6. Store image to AWS
                    length = 16
                    random_file_name = ''.join(random.choices(string.ascii_letters + string.digits, k=length))

                    file_name = f'{random_file_name}.jpg'
                    s3.upload_file("Python/current_frame/current_frame.jpg", bucket_name, file_name)
                    print("======================== IMAGE STORED TO AWS ========================")

                    #7. store info on database

                    print(f"Storing to database: {car_info["registrationNumber"]}, {car_info["make"]}, {car_info["colour"]}")
                    database.insertCar(car_info["registrationNumber"], car_info["make"], car_info["colour"], random_file_name)



        # 8. Clear the plates folder

        for file in os.listdir("Python/plates"):
            if os.path.exists(f'Python/plates/{file}'):
                os.remove(f'Python/plates/{file}')

    else:
        frame_counter += 1
    
    ret, frame = cap.read()

cap.release()
cv2.destroyAllWindows()