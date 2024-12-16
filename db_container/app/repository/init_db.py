from app.config import Config
from app.repository.database import Database

db = Database(region=Config.AWS_REGION)
