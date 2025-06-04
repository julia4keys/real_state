import requests,os
from bs4 import BeautifulSoup
import random

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium_stealth import stealth

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--disable-popup-blocking')
options.add_argument('--start-maximized')
options.add_argument('--disable-extensions')


# options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0")
# options.add_argument("accept=text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8")
# options.add_argument("accept-language=es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3")
# options.add_argument("dnt=1")
# options.add_argument("connection=keep-alive")
# options.add_argument("cookie=cookie-agreed=0")
# options.add_argument("upgrade-insecure-requests=1")
# options.add_argument("webdriver=1")
# options.add_argument("origin=https://www.google.es")
# options.add_argument("sec-ch-ua-mobile=?0")
#options.add_argument("content-type=application/json;charset=UTF-8")

HEADERS = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Cookie': 'cookie-agreed=0',
        'Upgrade-Insecure-Requests': '1'
    }


URL = 'https://www.idealista.com/pro/'

def fetch_ads(real_state: str, rent: bool = False):

    if rent:
        url = URL + real_state + '/alquiler-viviendas/'
    else:    
        url = URL + real_state + '/venta-viviendas/'
    data = {}
    #req = requests.get(url, headers=HEADERS)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    # Change the property value of the navigator for webdriver to undefined
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    user_agents = [
    # Add your list of user agents here
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
]

    # select random user agent
    user_agent = random.choice(user_agents)

    # pass in selected user agent as an argument
    options.add_argument(f'user-agent={user_agent}')

    #enable stealth mode
    stealth(driver,
        languages=["es-ES", "es"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )


    driver.get(url)
    print(url)
    print(driver.page_source)
    print(driver.execute_script("return navigator.userAgent"))
    
    # print(req.status_code)
    # print(req.text)
    # if req.status_code == 200:
    html = BeautifulSoup(driver.page_source, 'html.parser')
    ads = html.find_all('article', {'class': 'item-multimedia-container'})
    for i, ad in enumerate(ads):
        item = {'title': '', 'link': '', 'image': '', 'price': '', 'parking': '', 'detail': '', 'ellipsis': ''}
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
            im_buf = requests.get(tag_image['src'], headers=HEADERS)
            if im_buf.status_code == 200:
                folder = "./www/img/properties/"
                filename = folder + os.path.basename(tag_image['src'])
                with open(filename, mode="wb") as file:
                    file.write(im_buf.content)
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
        print(item)
    driver.close()
    return data



