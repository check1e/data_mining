from bs4 import BeautifulSoup
import requests
from urllib import parse
from pymongo import MongoClient

class MagnitParser:
    _headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 YaBrowser/20.9.1.112 Yowser/2.5 Safari/537.36",
        }
    _params = {
        'geo': 'moskva',
    }
    def __init__(self, start_url):
        self.start_url = start_url
        self._url = parse.urlparse(start_url)
        # self.__mongo_client = MongoClient('mongodb://user:pass@localhost:27017/db_name')
        mongo_client = MongoClient('mongodb://localhost:27017')
        self.db = mongo_client['parse_10']


    def _get_soup(self, url: str):
        response = requests.get(url, headers=self._headers)
        return BeautifulSoup(response.text, 'lxml')

    def parse(self):
        soup = self._get_soup(self.start_url)
        catalog = soup.find('div', attrs={'class': "сatalogue__main"})
        products = catalog.findChildren('a', attrs={'class': 'card-sale'})
        for product in products:
            if len(product.attrs.get('class')) > 2 or product.attrs.get('href')[0] != '/':
                continue
            product_url = f'{self._url.scheme}://{self._url.hostname}{product.attrs.get("href")}'
            product_soup = self._get_soup(product_url)
            product_data = self.get_product_structure(product_soup)
            self.save_to(product_data)

    def get_product_structure(self, product_tag):
        product_template = {
            'promo_name': ('div', 'action_title'),
            'product_name': '',
            'old_price': '',
            'new_price': '',
            'image_url': '',
            'date_from': '',
            'date_to': '',
        }
        product = {'url': url, }
        for key, value in product_template.items():
            try:
                product[key] = getattr(product_soup.find(value[0], attrs={'class': value[1]}), value[2])
            except Exception:
                product[key] = None
        # product_soup['product_name'] = product_soup.find('div', attrs={'class': 'action__title'}).text
        return product

    def parse_product_page(self, product):
        pass

    def save_to(self, product_data):
        collection = self.db['magnit']
        collection.insert_one(product_data)

        # for itm in collection.find({'promo_name': {'$regex':r'\d'}}):
        #     print(itm)
        # gt, lte, gte, lte,
        # https://docs.mongodb.com/manual/reference/operator/query/regex/
        pass

if __name__ == '__main__':
    url = 'https://magnit.ru/promo/?geo=moskva'
    parser = MagnitParser(url)
    parser.parse()