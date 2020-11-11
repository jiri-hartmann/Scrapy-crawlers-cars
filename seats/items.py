# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SeatsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    date = scrapy.Field()
    url = scrapy.Field()
    vin = scrapy.Field()
    price = scrapy.Field()
    created = scrapy.Field()
    km = scrapy.Field()
    car_type = scrapy.Field()
    color = scrapy.Field()
    url_ori = scrapy.Field()
