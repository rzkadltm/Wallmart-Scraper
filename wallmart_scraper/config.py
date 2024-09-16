# ------------------------ Variables ------------------------
BASE_URL = "https://www.walmart.com"
MAX_PAGE = 5

# ------------------------ Logging ------------------------

import os
import logging

if not os.path.exists('logs'):
    os.mkdir('logs')

LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'handlers': [
        logging.FileHandler('logs/wallmart_scraper.log'),
        logging.StreamHandler()
    ]
}

# ------------------------ Headers ------------------------

from fake_useragent import UserAgent
ua = UserAgent(os=["macos", "linux"], browsers="safari")
user_agent = ua.random

HEADERS={
    "Referer":"https://www.google.com",
    "Accept-Language":"en-US,en;q=0.9",
    "Accept-Encoding":"gzip, deflate, br",
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "User-Agent":user_agent
}