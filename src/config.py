import os
from dotenv import load_dotenv

load_dotenv()

ENTSOE_API_TOKEN = os.getenv("ENTSOE_API_KEY")
TIMEZONE = "Europe/Copenhagen"
AREA = "DK_WEST"
