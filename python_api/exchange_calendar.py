import requests
import json
from .cookie import Cookie
from . import time_helper


class CalendarQueryResult:

    Closed = 0
    Opened = 1
    Unkonwn = 2
    FatalError = 3


class ExchangeCalendar(Cookie):

    URL = {
        'cn': ['https://raw.githubusercontent.com/oniondata-site/calendar/main/data/cn.json',
               'https://gitee.com/oniondata-site/calendar/raw/main/data/cn.json']
    }

    def __init__(self, market_type, use_cn_mirror_site=False):
        super().__init__()
        self.value = self
        self.market_type = market_type
        self.use_cn_mirror_site = use_cn_mirror_site
        self.date_to_record = {}

    def load(self):
        self.date_to_record.clear()
        if not self.use_cn_mirror_site:
            url = self.URL[self.market_type][0]
        else:
            url = self.URL[self.market_type][1]

        json_text = fetch_url(url)
        record_list = json.loads(json_text)
        for record in record_list:
            date = record['date']
            self.date_to_record[date] = record

        # 每日的23:00:15刷新
        hms_list = [(23, 0, 15)]
        next_load_time = time_helper.filter_next_time(hms_list)
        self.set_end_time(next_load_time)

    def is_trade_date(self, date):
        if len(self.date_to_record) == 0:
            return CalendarQueryResult.FatalError

        record = self.date_to_record.get(date, None)
        if record is None:
            return CalendarQueryResult.Unkonwn

        if record['is_open'] == 1:
            return CalendarQueryResult.Opened
        else:
            return CalendarQueryResult.Closed


HEAD = {'User-Agent': 'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166  Safari/535.19', }


def fetch_url(url):
    for retry_time in range(5):
        try:
            response = requests.get(url, headers=HEAD, timeout=10)
            return response.text
        except Exception as ex:
            print(ex)
            pass

    print(f'fetch url[{url}] error! please check network status.')
    return None


calendar_dict = {}


def is_open(market_type, date=None, *, use_cn_mirror_site=False):
    # 参数
    assert(market_type in ('cn', ))
    if date is None:
        date = time_helper.get_today_date_text()

    calendar = calendar_dict.get(market_type, None)
    if calendar is None:
        calendar = ExchangeCalendar(market_type, use_cn_mirror_site=use_cn_mirror_site)
        calendar_dict[market_type] = calendar
    # 刷新缓存
    calendar.get_value()

    return calendar.is_trade_date(date)
