import scrapy
from seats.items import SeatsItem
import datetime as dt


class QuotesSpider(scrapy.Spider):
    name = "tipcars"
    start_urls = [
         'https://www.tipcars.com/skoda-superb/?mozny-odpocet-dph&servisni-'
         'knizka&2016-2019&350000-600000kc&-150000km&vybava=pohon-4x4,tazne-'
         'zarizeni,potahy-kuze,aut-prevodovka&str=1-500&text=l%26k',]

    def parse(self, response):
        htmls = response.xpath('//div[@class="blok sloupec_s_inzeratama"]'
                               '/a/@href').getall()
        yield from response.follow_all(htmls, callback=self.parse_car)

    def parse_car(self, response):
        item = SeatsItem()

        item['url'] = response.url
        item['date'] = str(dt.date.today())

        try:
            price = int(response.xpath('//div[contains(@class,"koncova_cena")]'
                                  '/b/text()').get().replace(" ", "")[:-2])
        except:
            price = None
        try:
            vin =  response.xpath('//div[contains(text(),"VIN")]'
                                '/following-sibling::div/text()'
                                  '').get().strip().replace('-', "")
        except AttributeError:
            vin = None
        try:
            created = response.xpath('//div[contains(text(),"vyrobeno")]'
                                '/following-sibling::div/text()').get().strip()
        except AttributeError:
            created = None
        try:
            km = int(response.xpath('//div[contains(text(),"tachometr")]'
                           '/following-sibling::div/text()'
                                '').get().replace(" ", "")[:-2])
        except:
            km = None
        try:
            car_type = response.xpath('//div[contains(text(),"karoserie")]'
                                '/following-sibling::div/text()').get().strip()
        except AttributeError:
            car_type = None
        try:
            color = response.xpath('//div[contains(text(),"barva")]'
                                '/following-sibling::div/text()').get().strip()
        except AttributeError:
            color = None
        try:
            url_ori = response.xpath('//div[contains(text(),"www")]'
                                  '/following-sibling::div/a/@href').get()
        except AttributeError:
            url_ori = None

        item['vin'] = vin
        item['price'] = price
        item['created'] = created
        item['km'] = km
        item['car_type'] = car_type
        item['color'] = color
        item['url_ori'] = url_ori

        yield item
