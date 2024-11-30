import os
from services.utils.config import Config
from dotenv import load_dotenv

load_dotenv()


class Config:
 ENDPOINT = os.getenv("ENDPOINT")
 KEY = os.getenv("SUBSCRIPTION_KEY") 
 AZURE_STOREGE_CONNECTION_STRING = os.getenv("AZURE_STOREGE_CONNECTION_STRING")
CONTAINER_NAME = os.environ.get("CONTAINER_NAME")