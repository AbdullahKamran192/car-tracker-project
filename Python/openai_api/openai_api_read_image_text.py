import base64
from openai import OpenAI
import os
from dotenv import find_dotenv, load_dotenv
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

client = OpenAI(
    api_key = os.getenv("OPEN_AI_API_KEY")
)

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def openai_read_image(image_path):

    # Getting the Base64 string
    base64_image = encode_image(image_path)


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

    return response.output_text