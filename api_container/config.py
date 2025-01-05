import json
from dotenv import load_dotenv
import os
import boto3
from botocore.exceptions import ClientError

load_dotenv()


def get_secret():
    secret_name = "holidays-secret"
    region_name = "us-west-2"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        return get_secret_value_response['SecretString']
    except ClientError as e:
        raise e


class Config:
    config_data_obj = json.loads(get_secret())
    GEMINI_API_KEY = config_data_obj['GEMINI_API_KEY']  # GEMINI_API_KEY
    AWS_REGION = config_data_obj['AWS_REGION']
    HOLIDAY_API_URL = config_data_obj['HOLIDAY_API_URL']
    DATABASE_HANDLER_URL = config_data_obj['DATABASE_HANDLER_URL']
