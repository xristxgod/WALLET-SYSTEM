from os import environ, path, listdir, mkdir
import logging

ENDPOINTS_URL_PATH = path.join(path.dirname(path.abspath(__file__)), 'files/endpoints_url.json')

logger = logging.getLogger(__name__)

class Config(object):
    DOMAINS = {x: y for x, y in environ.items() if x.startswith('DOMAIN_')}