from dotenv import load_dotenv
import os

# Load variables from the .env file
load_dotenv()

# Read the Gemini API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Model we'll use
MODEL_NAME = "gemini-2.5-flash"

# Data folder path
DATA_FOLDER = "data"
