import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from urllib.parse import urlparse
import time


class MagnitParser:
    _headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0",
    }
    _params = {
        'geo': 'moskva',
    }

    def __init__(self, start_url):
        self.start_url = start_url
        self._url = urlparse(start_url)
        mongo_client = MongoClient('mongodb://localhost:27017')
        self.db = mongo_client['magnit']

    def _get_soup(self, url: str):
        response = requests.get(url, headers=self._headers, params=self._params)
        return BeautifulSoup(response.text, 'lxml')

    def parse(self):
        soup = self._get_soup(self.start_url)
        catalog = soup.find('div', attrs={'class': 'сatalogue__main'})
        products = catalog.findChildren('a', attrs={'class': 'card-sale'})

        for product in products:
            if len(product.attrs.get('class')) > 2 or product.attrs.get('href')[0] != '/':
                continue
            time.sleep(0.1)
            product_url = f'{self._url.scheme}://{self._url.hostname}{product.attrs.get("href")}'
            product_soup = self._get_soup(product_url)
            product_data = self.get_product_structure(product_soup, product_url)
            self.save_to(product_data)
            print('Product parsed')

    def get_product_structure(self, product_soup, url):
        product_template = {
            'promo_name': ('p', 'action__name-text', 'text'),
            'product_name': ('div', 'action__title', 'text'),
            'old_price': ('div', 'label__price label__price_old', 'text'),
            'new_price': ('div', 'label__price label__price_new', 'text'),
            'image_url': ('img', 'action__image lazy', 'get'),
            'date_from': ('div', 'action__date-label', 'text'),
            'date_to': ('div', 'action__date-label', 'text'),
        }
        product = {'url': url}
        for key, value in product_template.items():
            try:
                if key == 'date_from':
                    prod = getattr(product_soup.find(value[0], attrs={'class': value[1]}), value[2])
                    product[key] = ' '.join(prod.split(' ')[1:3])
                #выясняем, есть ли слово price и тогда уже распарсиваем:
                elif key.count('price'):
                    prod = product_soup.findChild('div', attrs={'class': 'action__footer'})
                    product[key] = '.'.join(getattr(prod.find(value[0], attrs={'class': value[1]}), value[2]).split())
                elif key == 'image_url':
                    prod = getattr(product_soup.find(value[0], attrs={'class': value[1]}), value[2])('data-src')
                    product[key] = f'{urlparse(url).scheme}://{urlparse(url).hostname}{prod}'

                elif key == 'date_to':
                    prod = getattr(product_soup.find(value[0], attrs={'class': value[1]}), value[2])
                    product[key] = ' '.join(prod.split(' ')[-2:])
                else:
                    product[key] = getattr(product_soup.find(value[0], attrs={'class': value[1]}), value[2])
            except Exception:
                product[key] = None
        return product

    def save_to(self, product_data: dict):
        collection = self.db['magnit']
        collection.insert_one(product_data)

if __name__ == '__main__':
    url = 'https://magnit.ru/promo/'
    parser = MagnitParser(url)
    parser.parse()