from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from instaparser.spiders.instagram import InstagramSpider
from instaparser import settings

import os
from dotenv import load_dotenv
load_dotenv('.env')


if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)

    users = ['go_chatbot', '_.the_lashes._']
    process.crawl(InstagramSpider, login=os.getenv('LOGIN'), enc_password=os.getenv('ENC_PASSWORD'))

    process.start()
