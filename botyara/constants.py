import os
from dotenv import load_dotenv

load_dotenv()

DATABASE = "../database/"
TOKEN = os.getenv("TELEGRAM_TOKEN")
