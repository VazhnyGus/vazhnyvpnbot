import os
from dotenv import load_dotenv, set_key


class Config:
    def __init__(self) -> None:
        load_dotenv()
        self.bot_token = os.getenv("BOT_TOKEN")
        self.database_url = os.getenv("DATABASE_URL")
        self.outline_api_url = os.getenv("OUTLINE_API_URL")
        self.outline_api_cert = os.getenv("OUTLINE_API_CERT")
        self.admin_password = os.getenv("ADMIN_PASSWORD")

    def set_admin_password(self, password: str):
        set_key(".env", "ADMIN_PASSWORD", password)
        self.admin_password = password

config = Config()
