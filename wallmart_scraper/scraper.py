import requests
import logging
import json
from bs4 import BeautifulSoup
from wallmart_scraper.config import LOGGING_CONFIG, BASE_URL, HEADERS, MAX_PAGE

logging.basicConfig(**LOGGING_CONFIG)
logger = logging.getLogger(__name__)

class WallmartScraper:
    def __init__(self):
        self.base_url = BASE_URL
        self.headers = HEADERS
        self.current_page = 1

    def get_all_products(self, query, page=1):
        link_query = f"{self.base_url}/search?q={query}&page={page}"
        product_links = []
        link_on_page = 0

        while self.current_page <= MAX_PAGE:
            try:
                logger.info("Fetching product link on page: {page}...")
                response = requests.get(link_query, headers=self.headers)
                response.raise_for_status()

                soup = BeautifulSoup(response.text, "html.parser")
                links = soup.find_all("a", href=True)
                
                for link in links:
                    link_href = link.get("href")
                    if "/ip/" in link_href:
                        if "https://" in link_href:
                            link_product = link_href
                        else:
                            link_product = self.base_url + link_href
                        
                        link_on_page += 1
                        product_links.append(link_product)
                
                logger.info(f"Retrieved {link_on_page} product links on page: {page}")
            
            except requests.exceptions.RequestException as e:
                logger.error(f"Network error occurred: {e}", exc_info=True)
            except Exception as e:
                logger.error(f"An unexpected error occurred: {e}", exc_info=True)
            finally:
                self.current_page += 1

        return product_links

    def extract_product_info(self, wallmart_url):
        try:
            logger.info(f"Fetching product information from...")
            response = requests.get(wallmart_url, headers=self.headers)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            script_tag = soup.find("script", id="__NEXT_DATA__")
            if not script_tag:
                raise ValueError("Script tag with id '__NEXT_DATA__' not found.")
            
            logger.info(f"Retrieved product information from...")
            data = json.loads(script_tag.string)
            initial_data = data["props"]["pageProps"]["initialData"]["data"]
            product_data = initial_data["product"]
            reviews_data = initial_data.get("reviews", {})

            product_info = {
                "price": product_data["priceInfo"]["currentPrice"]["price"],
                "review_count": reviews_data.get("totalReviewCount", 0),
                "item_id": product_data["usItemId"],
                "avg_rating": reviews_data.get("averageOverallRating", 0),
                "product_name": product_data["name"],
                "brand": product_data.get("brand", ""),
                "availability": product_data["availabilityStatus"],
                "image_url": product_data["imageInfo"]["thumbnailUrl"],
                "short_description": product_data.get("shortDescription", "")
            }
            
            return product_info

        except requests.exceptions.RequestException as e:
            logger.error(f"Network error occurred: {e}", exc_info=True)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON: {e}", exc_info=True)
        except KeyError as e:
            logger.error(f"Key error: Missing key in JSON data - {e}", exc_info=True)
        except ValueError as e:
            logger.error(f"Value error: {e}", exc_info=True)
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}", exc_info=True)

        return None
    
    def write_data_to_jsonl(self, dict_data, query):
        try:
            data = json.dumps(dict_data)
            with open(f"data/{query}_data.jsonl", "a") as f:
                f.write(f"{data}\n")
                
        except TypeError as e:
            logger.error(f"Failed to serialize JSON: {e}", exc_info=True)
        except IOError as e:
            logger.error(f"File I/O error: {e}", exc_info=True)
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}", exc_info=True)