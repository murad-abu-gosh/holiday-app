import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017')
    MONGO_DB_NAME = os.getenv('MONGO_DB_NAME', 'holiday_db')
    HOLIDAY_API_KEY = os.getenv('HOLIDAY_API_KEY', '')
    HOLIDAY_API_URL = 'https://holidays.abstractapi.com/v1/'
    GEMINI_API_KEY = "AIzaSyCm97Bj5ZXfmKWeh7KpL0wL80uom6afAUE"
    AWS_REGION = "eu-central-1"