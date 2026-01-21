import boto3
from dotenv import load_dotenv
import os

#Load environment variables from the .env file (if present)
load_dotenv()

AWS_S3_BUCKET_NAME = os.getenv('BUCKET_NAME')
AWS_REGION = os.getenv('eu-north-1')
AWS_ACCESS_KEY = os.getenv('ACCESS_KEY')
AWS_SECRET_KEY = os.getenv('SECRET_ACCESS_KEY')


s3_client = boto3.client(
        service_name='s3',
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY
)

def upload_number_plate_to_s3(file_path, file_name):
    response = s3_client.upload_file(file_path, AWS_S3_BUCKET_NAME, file_name)