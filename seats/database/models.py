from sqlalchemy import Column, String, Integer, Date, DateTime
from sqlalchemy.ext.declarative import declarative_base

DeclarativeBase = declarative_base()


class AllData(DeclarativeBase):
    __tablename__ = 'seats'

    idd = Column(Integer, primary_key=True)
    date = Column(Date)
    url = Column(String(255))
    vin = Column(String(127))
    price = Column(Integer)
    created = Column(String(127))
    km = Column(Integer)
    car_type = Column(String(127))
    color = Column(String(127))
    url_ori = Column(String(127))

    def __init__(self, idd=None, date=None, url=None, vin=None, price=None,
                 created=None, km=None, car_type=None, color=None,
                 url_ori=None):
        self.idd = idd
        self.date = date
        self.url = url
        self.vin = vin
        self.price = price
        self.created = created
        self.km = km
        self.car_type = car_type
        self.color = color
        self.url_ori = url_ori

    def __repr__(self):
        ret_string = f"<AllData: idd={self.idd},date={self.date}, url={self.url}, " \
                     f"vin={self.vin}, price={self.price}, created" \
                     f"={self.created}, km={self.km}, car_type=" \
                     f"{self.car_type}, color={self.color}, url_ori" \
                     f"={self.url_ori},>"
        return ret_string