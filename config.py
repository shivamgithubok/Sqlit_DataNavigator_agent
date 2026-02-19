import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()


BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / ".env"

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")