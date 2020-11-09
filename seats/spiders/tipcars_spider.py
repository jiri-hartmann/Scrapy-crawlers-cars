import scrapy
import datetime as dt
import sqlalchemy
import pandas as pd
import keyring
class QuotesSpider(scrapy.Spider):
    name = "tipcars"
    start_urls = [
         'https://www.tipcars.com/skoda-superb/?mozny-odpocet-dph&servisni-'
         'knizka&2016-2019&350000-600000kc&-150000km&vybava=pohon-4x4,tazne-'
         'zarizeni,potahy-kuze,aut-prevodovka&str=1-500&text=l%26k',]

    service = "MariaDB" # name of service in Windows valet
    user="root"
    db_name="ades"
    db_server='localhost'
    password = keyring.get_password(service, user)
    if not password:
        password = input(f'Input password to system {service} for user {user}: ')
        keyring.set_password(service, user, password)
    conn_string = f"mysql+pymysql://{user}:{password}@{db_server}/{db_name}"
    alchemy_conn = sqlalchemy.create_engine(conn_string)
    first_day_for_import = alchemy_conn.execute("select max(`date`) from seats").fetchone()[0] + dt.timedelta(days=1)

    def parse(self, response):
        filename = 'tipcars.html'
        htmls = response.xpath('//div[@class="blok sloupec_s_inzeratama"]'
                               '/a/@href').getall()
        with open(filename, 'w') as f:
            for html in htmls:
                f.write('https://www.tipcars.com' + html + '\n')

        yield from response.follow_all(htmls, callback=self.parse_car)

    def parse_car(self, response):
        global first_day_for_import
        global alchemy_conn
        
        url = response.url
        date = str(dt.date.today())

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
            type = response.xpath('//div[contains(text(),"karoserie")]'
                                '/following-sibling::div/text()').get().strip()
        except AttributeError:
            type = None
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

        result = {'date': date,
               'url': url,
               'vin': vin,
               'price': price,
               'created': created,
               'km': km,
               'type': type,
               'color': color,
               'url_ori': url_ori
               }

        df = pd.DataFrame(result, index=[0])
        if first_day_for_import <= dt.date.today():
            df.to_sql("seats", alchemy_conn, if_exists="append", index=False)

        yield result
