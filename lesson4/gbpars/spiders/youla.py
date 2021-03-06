import scrapy
from pymongo import MongoClient

class YoulaSpider(scrapy.Spider):
    name = 'youla1'
    allowed_domains = ['auto.youla.ru']
    start_urls = ['https://auto.youla.ru/']
    xpath = {
        'brands': '//div[@class="TransportMainFilters_brandsList__2tIkv"]//a[@class="blackLink"]/@href'
        ,'ads': '//div[@id="serp"]//article//a[@data-target="serp-snippet-title"]/@href'
        ,'pagination': '//div[contains(@class, "Paginator_block")]/a/@href'
        ,
    }
    db_client = MongoClient()

    def parse(self, response, **kwargs):
        for url in response.xpath(self.xpath['brands']):
            yield response.follow(url, callback=self.brand_parse)

    def brand_parse(self, response, **kwargs):
        for url in response.xpath(self.xpath['pagination']):
            yield response.follow(url, callback=self.brand_parse)

        for url in response.xpath(self.xpath['ads']):
            yield response.follow(url, callback=self.ads_parse)

    def ads_parse(self, response, **kwargs):
        name = response.xpath('//div[contains(@class, "AdvertCard_advertTitle")]/text()').extract_first()
        images = response.xpath('//div[contains(@class, "PhotoGallery_block")]//img/@src').extract()
        attrs_labels = response.xpath('//div[contains(@class, "AdvertSpecs_row__")]//div[contains(@class, "AdvertSpecs_label__")]//text()').extract()
        attrs_data = response.xpath('//div[contains(@class, "AdvertSpecs_row__")]//div[contains(@class, "AdvertSpecs_data__")]//text()').extract()
        attrs = dict(zip(attrs_labels, attrs_data))
        text = response.xpath('//div[contains(@class, "AdvertCard_descriptionInner")]/text()').extract_first()


        #https: // auto.youla.ru / api / profile / youla?userId = 19268359
        #Only works for mobile devices.
        #author = response.xpath('').extract()
        #phone = response.xpath(').extract()

        # процедура соранения в БД
        collection = self.db_client['parse_10'][self.name]
        collection.insert_one({'title': name, 'img': images, 'attrs': attrs, 'text': text})