import requests
from bs4 import BeautifulSoup





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
    req = requests.get(url, headers=HEADERS)
    if req.status_code == 200:
        html = BeautifulSoup(req.text, 'html.parser')
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
                item['image'] = tag_image['src']
            if tag_price:
                item['price'] = tag_price.getText().strip('\n')
            if tag_parking:    
                item['parking'] = tag_parking.getText().strip('\n')
            if tag_detail:
                item['detail'] = tag_detail.getText().strip('\n')     
            if tag_ellipsis:
                item['ellipsis'] = tag_ellipsis.getText().strip('\n')
            data[i] = item
    return data



