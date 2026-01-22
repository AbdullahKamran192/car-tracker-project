import base64
import cv2
from openai import OpenAI
import os
from dotenv import find_dotenv, load_dotenv
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

client = OpenAI(
    api_key = os.getenv("OPEN_AI_API_KEY")
)

# Function to encode the image
def encode_plate_image(plate_image):
    success, buffer = cv2.imencode(".jpg", plate_image)

    if not success:
        raise ValueError("Failed to encode plate image as .jpg")
    
    return base64.b64encode(buffer).decode("utf-8")

def openai_read_image(array_of_plates_images):

    array_of_plates_text = []

    for plate_image in array_of_plates_images:
        # Getting the Base64 string
        base64_image = encode_plate_image(plate_image)
        
        response = client.responses.create(
            model="gpt-4.1",
            input=[
                {
                    "role": "user",
                    "content": [
                        { "type": "input_text", "text": "Just only return the car's number plate text. example 'BD55 JFY', not 'the car's number plate is ''BD55 JFY'' or other text. Only car plate text shown in the image"},
                        {
                            "type": "input_image",
                            "image_url": f"data:image/jpeg;base64,{base64_image}",
                        },
                    ],
                }
            ],
        )
        plate_text = response.output_text.replace(' ', '')

        array_of_plates_text.append(plate_text)

    return array_of_plates_text