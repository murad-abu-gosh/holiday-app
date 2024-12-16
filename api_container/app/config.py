import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    HOLIDAY_API_KEY = os.getenv('HOLIDAY_API_KEY', '')
    HOLIDAY_API_URL = 'https://holidays.abstractapi.com/v1/'
    GEMINI_API_KEY = "AIzaSyCm97Bj5ZXfmKWeh7KpL0wL80uom6afAUE"
    AWS_REGION = 'eu-central-1'
    DATABASE_HANDLER_URL = "http://<DB_HANDLER_IP>:5001"