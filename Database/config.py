import os
import logging

logger = logging.getLogger(__name__)

class Config:
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:mamedov00@localhost/telegram_bot_system")
    DATABASE_INTERFACE_SECRET_KEY = os.getenv("DATABASE_INTERFACE_SECRET_KEY", "F441sfa1hshqsaflkasknlvonsd34124")
    DATABASE_INTERFACE_PASSWORD = os.getenv("DATABASE_INTERFACE_PASSWORD", "admin")
    DATABASE_INTERFACE_GOOGLE_AUTH_SECRET_KEY = os.getenv("DATABASE_INTERFACE_GOOGLE_AUTH_SECRET_KEY", "OBYE232HOFKHGWDS")