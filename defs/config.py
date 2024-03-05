import os

from dotenv import load_dotenv

load_dotenv()

COOKIES = os.environ.get("COOKIES")
GENSHIN_PLAYER_ID = int(os.environ.get("GENSHIN_PLAYER_ID"))
GENSHIN_GENDER_BOY = os.environ.get("GENSHIN_GENDER_BOY") == "true"
DOMAIN = os.environ.get("DOMAIN")
