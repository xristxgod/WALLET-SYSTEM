import os

class Config(object):

    DATABASE_URL = os.getenv("DATABASE_URL")
    DOMAIN_TRON_API = os.getenv("DOMAIN_TRON_API")
    DOMAIN_BOT_ALERT = os.getenv("DOMAIN_BOT_ALERT")
    DOMAIN_DATABASE_INTERFACE = os.getenv("DOMAIN_DATABASE_INTERFACE")