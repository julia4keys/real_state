import requests,os,time
from bs4 import BeautifulSoup
import random

from seleniumbase import Driver
from seleniumbase import sb_cdp


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

def fetch_ads(real_state: str, rent: bool = False):

    if rent:
        url = URL + real_state + '/alquiler-viviendas/'
    else:    
        url = URL + real_state + '/venta-viviendas/'
    data = {}
    driver = Driver(uc=True)
    driver.uc_open_with_reconnect(url, reconnect_time=4)
    #sb = sb_cdp.Chrome(url, geoloc=(48.87645, 2.26340))
    print(driver.page_source)

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
            time.sleep(random.choice([1, 4, 6, 8, 10, 12]))
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



