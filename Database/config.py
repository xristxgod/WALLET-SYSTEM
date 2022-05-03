import os
import logging

logger = logging.getLogger(__name__)

class Config:
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:mamedov00@localhost/telegram_bot_system")