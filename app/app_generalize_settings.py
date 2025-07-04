import os
from dotenv import load_dotenv,find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file
from agno.models.google import Gemini

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY',None)
# === DRIVE CONFIG ===
SCOPES = ["https://www.googleapis.com/auth/drive"]
FOLDER_NAME = "BMVSI_HR_POLICIES"
CACHE_FILE = "tmp/pdf_url_cache.json"
# Email setup
NOTIFIER_EMAIL = os.getenv('NOTIFIER_EMAIL')
NOTIFIER_EMAIL_PASSWORD = os.getenv('NOTIFIER_EMAIL_PASSWORD')
HR_EMAILS = os.getenv('HR_EMAILS')
CC_EMAILS = os.getenv('CC_EMAILS')
# Initialize the Gemini model client
MODEL=Gemini(id="gemini-2.0-flash",api_key=GEMINI_API_KEY)