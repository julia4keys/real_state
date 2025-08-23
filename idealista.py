import requests,os,time
from bs4 import BeautifulSoup
import random

from seleniumbase import Driver


URL = 'https://www.idealista.com/pro/'

def fetch_ads(real_state: str, rent: bool = False):

    if rent:
        url = URL + real_state + '/alquiler-viviendas/'
    else:    
        url = URL + real_state + '/venta-viviendas/'
    data = {}
    #req = requests.get(url, headers=HEADERS)
    #driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver = Driver(uc=True, headless=True)
    driver.uc_open_with_reconnect(url, reconnect_time=4)
    #print(url)
    print(driver.page_source)
    #print(driver.execute_script("return navigator.userAgent"))
    
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
            time.sleep(5)
            im_buf = requests.get(tag_image['src'])#, headers=HEADERS)
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



