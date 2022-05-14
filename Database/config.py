from os import environ
from typing import Tuple

class Config(object):
    DATABASE_URL = environ.get("DATABASE_URL", "postgresql://postgres:mamedov00@localhost/telegram_bot_system")
    DATABASE_INTERFACE_PASSWORD = environ.get("DATABASE_INTERFACE_PASSWORD", "admin")
    DATABASE_INTERFACE_GOOGLE_AUTH_SECRET_KEY = environ.get("DATABASE_INTERFACE_GOOGLE_AUTH_SECRET_KEY", "https://medium.com/aubergine-solutions/quick-start-two-factor-authentication-in-django-admin-panel-d15ceeb62591")
    DATABASE_INTERFACE_SECRET_KEY = environ.get("DATABASE_INTERFACE_SECRET_KEY", "django-insecure-yc25#g4+l$6_@q(41ct2d9zd@o!w4+yt&v8q68hv*esav^k-9n")

def get_db_config(url: str = Config.DATABASE_URL) -> Tuple:
    user = url.split(":")[1].replace("//", "")
    password = url.split(":")[2].split("@")[0]
    host = url.split(":")[2].split("@")[1].split("/")[0]
    port = url.split(":")[3].split("/")[0] if host != "localhost" else None
    db_name = url.split(":")[3].split("/")[1] if port else url.split(":")[2].split("/")[1]
    return user, password, host, port, db_name

USER, PASSWORD, HOST, PORT, DB_NAME = get_db_config()