import requests
import os
from dotenv import find_dotenv, load_dotenv
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

url = "https://driver-vehicle-licensing.api.gov.uk/vehicle-enquiry/v1/vehicles"

def get_car_info(reg_number):
    
    #payload = "{\n\t\"registrationNumber\": \"LG15GRF\"\n}"
    payload = {"registrationNumber": f"{reg_number}"}
    headers = {
        'x-api-key': os.getenv("DVLA_API_KEY"),
        'Content-Type': 'application/json'
    }

    try:
     response = requests.request("POST", url, headers=headers, json=payload)

     if response.status_code != 200:
        return None
     
    except KeyError:
       print(f"{reg_number} is NOT a correct reg plate")
    except Exception:
       print("Something went wrong. car info could not be fetched.")
    data = response.json()

    return data