import cloudinary
import os
from dotenv import load_dotenv


load_dotenv(dotenv_path='../../.env')

CLOUD_NAME = os.getenv("CLOUD_NAME")
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

cloudinary.config(
    cloud_name="dbrhihytl",
    api_key="212724769336457",
    api_secret="7wCEBQZ59fpTnjVPWyolJYEIlrM",
    secure=True
)
