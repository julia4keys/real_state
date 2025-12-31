import requests
import os
import time
import random
import logging
from bs4 import BeautifulSoup
from seleniumbase import Driver

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
URL = 'https://www.idealista.com/pro/'
HEADERS = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Cookie': 'cookie-agreed=0',
        'Upgrade-Insecure-Requests': '1'
    }

def setup_driver():
    """Configures and returns a browser instance."""
    driver = Driver(uc=True)
    return driver

def download_image(image_url, folder):
    """Downloads an image and saves it to the specified folder."""
    try:
        response = requests.get(image_url, headers=HEADERS)
        if response.status_code == 200:
            filename = os.path.join(folder, os.path.basename(image_url))
            os.makedirs(folder, exist_ok=True)
            with open(filename, mode="wb") as file:
                file.write(response.content)
            return filename
    except Exception as e:
        logger.error(f"Error downloading image {image_url}: {e}")
    return None

def fetch_ads(real_state: str, rent: bool = False):
    """Extracts property ads from Idealista."""
    if rent:
        url = URL + real_state + '/alquiler-viviendas/'
    else:    
        url = URL + real_state + '/venta-viviendas/'

    data = {}
    driver = setup_driver()
    try:
        driver.uc_open_with_reconnect(url, reconnect_time=4)
        html = BeautifulSoup(driver.page_source, 'html.parser')
        ads = html.find_all('article', {'class': 'item-multimedia-container'})

        for i, ad in enumerate(ads):
            item = {
                'title': '',
                'link': '',
                'image': '',
                'price': '',
                'parking': '',
                'detail': '',
                'ellipsis': ''
            }

            tag_link = ad.find('a', {'class': 'item-link'})
            tag_image = ad.find('img')
            tag_price = ad.find('span', {'class': 'item-price'})
            tag_parking = ad.find('span', {'class': 'item-parking'})
            tag_detail = ad.find('span', {'class': 'item-detail'})
            tag_ellipsis = ad.find('p', {'class': 'ellipsis'})
            if tag_link:
                item['title'] = tag_link.getText().strip('\n')
                item['link'] = 'https://www.idealista.com' + tag_link['href']
            if tag_image:
                time.sleep(random.choice([1, 4, 6, 8, 10, 12]))
                image_path = download_image(tag_image['src'], "./www/img/properties/")
                if image_path:
                    item['image'] = "img/properties/" + os.path.basename(tag_image['src'])
            if tag_price:
                item['price'] = tag_price.getText().strip('\n')
            if tag_parking:
                item['parking'] = tag_parking.getText().strip('\n')

            if tag_detail:
                item['detail'] = tag_detail.getText().strip('\n')

            if tag_ellipsis:
                item['ellipsis'] = tag_ellipsis.getText().strip('\n')

            data[i] = item
            logger.info(f"Ad {i}: {item}")
            print(f"Ad {i}: {item}")

    except Exception as e:
        logger.error(f"Error fetching ads: {e}")
    finally:
        driver.close()
    return data

if __name__ == "__main__":
    # Example usage
    ads = fetch_ads("madrid", rent=False)
    print(ads)



