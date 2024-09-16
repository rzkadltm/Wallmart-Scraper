import pdb
import logging
from wallmart_scraper.scraper import WallmartScraper
from wallmart_scraper.config import LOGGING_CONFIG

logging.basicConfig(**LOGGING_CONFIG)
logger = logging.getLogger(__name__)

product_keywords = [
    "Laptop",
    "Headphones",
    "Coffee Maker",
    "Smartphone",
    "Backpack",
]

def main():
    logger.info("Wallmart Scraper is started....")
    scraper = WallmartScraper()
    for keyword in product_keywords:
        urls = scraper.get_all_products(keyword)
        for url in urls:
            product = scraper.extract_product_info(url)
            scraper.write_data_to_jsonl(product, keyword)

if __name__ == "__main__":
    main()