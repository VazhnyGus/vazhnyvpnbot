import os


class Config:
    def __init__(self) -> None:
        self.bot_token = os.getenv("BOT_TOKEN")
        self.database_url = os.getenv("DATABASE_URL")
        self.outline_api_url = os.getenv("OUTLINE_API_URL")
        self.outline_api_cert = os.getenv("OUTLINE_API_CERT")
        self.admin_password = os.getenv("ADMIN_PASSWORD")

config = Config()
