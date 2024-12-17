import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017')
    MONGO_DB_NAME = os.getenv('MONGO_DB_NAME', 'holiday_db')
    HOLIDAY_API_KEY = os.getenv('HOLIDAY_API_KEY', '')
    HOLIDAY_API_URL = 'http://localhost:5002'
    GEMINI_API_KEY = "AIzaSyCm97Bj5ZXfmKWeh7KpL0wL80uom6afAUE"
    AWS_REGION = 'us-west-2'
    DATABASE_HANDLER_URL = "http://localhost:5001"