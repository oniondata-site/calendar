from sqlalchemy import Column, String, Integer, Float, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import DOUBLE


Model = declarative_base()
engine = None
Session = None


def init_database_connect():
    global engine
    global Session
    DB_CONNECT_CONFIG = 'mysql+mysqlconnector://root:mysql_20210617@192.168.11.15:3306/calendar_db?charset=utf8;auth_plugin=mysql_native_password'
    engine = create_engine(DB_CONNECT_CONFIG, echo=False, pool_recycle=3600)
    Session = sessionmaker(bind=engine)


init_database_connect()


class DateEventRecord(Model):

    __abstract__ = True  # 关键语句,定义所有数据库表对应的父类
    __table_args__ = {"extend_existing": True}  # 允许表已存在

    date = Column(String(10), primary_key=True, nullable=False)
    is_open = Column(Integer, nullable=False, default=1)
    comment = Column(String(200), nullable=False, default='')

    exchange_name_to_class = {}

    def to_dict(self):
        return {'date': self.date, 'is_open': self.is_open, 'comment': self.comment}

    @classmethod
    def make_class(cls, exchange_name):
        if exchange_name in cls.exchange_name_to_class:
            return cls.exchange_name_to_class[exchange_name]

        exchange_name_cls = type(f'CodeNameRecord_{exchange_name}', (DateEventRecord, ), {'__tablename__': exchange_name})
        Model.metadata.create_all(engine)
        cls.exchange_name_to_class[exchange_name] = exchange_name_cls

        return exchange_name_cls


class ExchangeCalendar:

    def __init__(self, exchange_name, *, session=None, load_when_init=True):
        self.exchange_name = exchange_name
        self.session = session
        self.records = None
        self.DateEventRecordClass = DateEventRecord.make_class(exchange_name)
        # 映射
        self.date_to_record = {}
        if load_when_init:
            self.load()

    def get_value(self):
        if self.records is None:
            self.load()

        return self.records

    def load(self):
        # load from database
        if self.session is None:
            with Session() as session:
                self.records = session.query(self.DateEventRecordClass).all()
        else:
            self.records = self.session.query(self.DateEventRecordClass).all()
        self.after_loaded()

    def after_loaded(self):
        self.date_to_record.clear()
        for index, record in enumerate(self.records):
            record.index = index
            self.date_to_record[record.date] = record

    def retrieve_record(self, date):
        return self.date_to_record.get(date, None)

    def nearest_trade_date(self, date, offset=0):
        start_record = self.date_to_record.get(date, None)
        if start_record is None:
            return None
        # 往前回溯
        start_index = start_record.index
        while True:
            if start_record.is_open == 1:
                break
            if start_index >= 0:
                start_record = self.records[start_index]
            else:
                return None
            start_index -= 1
        # offset
        if offset == 0:
            return start_record.date
        # 向左遍历
        target_index = start_record.index
        target_record = start_record
        while offset < 0:
            target_index -= 1
            if target_index >= 0:
                target_record = self.records[target_index]
            else:
                return None
            if target_record.is_open == 1:
                offset += 1
        while offset > 0:
            target_index += 1
            if target_index < len(self.records):
                target_record = self.records[target_index]
            else:
                return None
            if target_record.is_open == 1:
                offset -= 1
        return target_record.date
