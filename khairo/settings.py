import os
from dotenv import load_dotenv
load_dotenv(dotenv_path="./env")
DEBUG = os.getenv("DEBUG")
SECRET_KEY = os.getenv("SECRET_KEY")
REFRESH_KEY = os.getenv("REFRESH_KEY")
EMAIL = os.getenv("EMAIL")
BUCKET_NAME = os.getenv("bucket")
PASSWORD = os.getenv("PASSWORD")
ACCESS_TOKEN_EXPIRE_TIME = os.getenv("ACCESS_TOKEN_EXPIRE_TIME")
REFRESH_TOKEN_EXPIRE_TIME = os.getenv("REFRESH_TOKEN_EXPIRE_TIME")
WEBSITE_URL = "http://127.0.0.1:8000"
WEBSITE_NAME = "khairo"
API_BASE_URI = "/api/v1"
BASE_DIR =os.path.dirname(os.path.realpath(__file__))


