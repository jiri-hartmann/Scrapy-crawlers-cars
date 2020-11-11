# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from seats.database.connection import db
from seats.database.models import AllData
from sqlalchemy import and_


class SeatsPipeline:
    def process_item(self, item, spider):
        # create a new SQL Alchemy object and add to the db session
        record = AllData(date=item['date'],
                         url=item['url'],
                         vin=item['vin'],
                         price=item['price'],
                         created=item['created'],
                         km=item['km'],
                         car_type=item['car_type'],
                         color=item['color'],
                         url_ori=item['url_ori']
                         )

        db.add(record)
        db.commit()

        return item
