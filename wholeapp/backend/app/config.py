import os
from dotenv import load_dotenv
load_dotenv()
class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback")
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "flaskshield")
    JWT_SECRET = os.getenv("JWT_SECRET", "fallback_jwt_secret")
    ACCESS_EXPIRES = int(os.getenv("ACCESS_EXPIRES", 900))
    REFRESH_EXPIRES = int(os.getenv("REFRESH_EXPIRES", 604800))
