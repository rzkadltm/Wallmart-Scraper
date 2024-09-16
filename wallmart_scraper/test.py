import logging
from config import LOGGING_CONFIG

logging.basicConfig(**LOGGING_CONFIG)
logger = logging.getLogger(__name__)

try:
    a = 1
    logging.info(f"Success")
    try:
        logging.debug(f"Insert 3 to variable a")
        a = 3
        try:
            a = 3
            a[3]=3
            logging.debug(f"Insert 3 to variable a")
        except Exception as e:
            logging.error(f"Error {e}")  
    except Exception as e:
        logging.error(f"Error {e}")  
except Exception as e:
    logging.error(f"Failed {e}")