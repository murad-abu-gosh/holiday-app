<<<<<<< HEAD
import os
=======
import json
>>>>>>> 9e81978995a17891b14d75beb97720afe18efabe

from dotenv import load_dotenv

load_dotenv()

<<<<<<< HEAD

class Config:
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017')
    MONGO_DB_NAME = os.getenv('MONGO_DB_NAME', 'holiday_db')
    HOLIDAY_API_KEY = os.getenv('HOLIDAY_API_KEY', '')
    HOLIDAY_API_URL = 'http://localhost:5002'
    GEMINI_API_KEY = "AIzaSyCm97Bj5ZXfmKWeh7KpL0wL80uom6afAUE"
    AWS_REGION = 'us-west-2'
    DATABASE_HANDLER_URL = "http://localhost:5001"
=======
# Use this code snippet in your app.
# If you need more information about configurations
# or implementing the sample code, visit the AWS docs:
# https://aws.amazon.com/developer/language/python/

import boto3
from botocore.exceptions import ClientError


def get_secret():
    secret_name = "holiday_secrets"
    region_name = "us-west-2"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    secret = get_secret_value_response['SecretString']

    # Your code goes here.

    return secret


class Config:
    config_data_obj = json.loads(get_secret())
    GEMINI_API_KEY = config_data_obj['GEMINI_API_KEY']  # GEMINI_API_KEY
    AWS_REGION = config_data_obj['AWS_REGION']
    HOLIDAY_API_URL = config_data_obj['HOLIDAY_API_URL']
    DATABASE_HANDLER_URL = config_data_obj['DATABASE_HANDLER_URL']
>>>>>>> 9e81978995a17891b14d75beb97720afe18efabe
