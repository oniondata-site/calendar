import requests
import json
from .cookie import Cookie
from . import time_helper
from .redis_client import create_redis_client


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

    def __init__(self, market_type, *, use_redis_mirror=True, use_cn_mirror_site=False):
        super().__init__()
        self.value = self
        self.market_type = market_type
        self.use_redis_mirror = use_redis_mirror
        self.use_cn_mirror_site = use_cn_mirror_site
        self.date_to_record = {}

    def load(self):
        ''' 优先级，redis > git
        '''
        self.date_to_record.clear()
        while True:
            # redis
            client = None
            if self.use_redis_mirror:
                client = create_redis_client()
            if client is not None:
                json_text = client.hget('calendar', 'cn.json')
                break
            # http
            if not self.use_cn_mirror_site:
                url = self.URL[self.market_type][0]
            else:
                url = self.URL[self.market_type][1]
            json_text = fetch_url(url)
            break

        record_list = json.loads(json_text)
        for record in record_list:
            date = record['date']
            self.date_to_record[date] = record

        # 每日的23:00:15刷新
        hms_list = [(23, 0, 15)]
        next_load_time = time_helper.filter_next_time(hms_list)
        self.set_end_time(next_load_time)

    def query_date_status(self, date):
        if len(self.date_to_record) == 0:
            return CalendarQueryResult.FatalError

        record = self.date_to_record.get(date, None)
        if record is None:
            return CalendarQueryResult.Unkonwn

        if record['is_open'] == 1:
            return CalendarQueryResult.Opened
        else:
            return CalendarQueryResult.Closed


HEAD = {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Mobile Safari/537.36', 
    'Referer': 'https://gitee.com/oniondata-site/calendar/blob/main/data/cn.json'}


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


def query_date_status(market_type, date=None, *, use_cn_mirror_site=False):
    '''
    查询某日的日历

    Parameters:
        market_type - 市场类型，字符串。可选，'cn', 'hk', 'us'
        date - 日期，字符串。比如，'20200101'
        use_redis_mirror - 是否使用 redis 镜像源。预防 github 和 gitee 同时无法访问。
                         - 默认是，需要自行（搭建 redis => 同步数据 => 修改 config.json）才会生效。
        use_cn_mirror_site - 是否使用位于中国的镜像网站加速。强烈推荐国内网络勾选此项

    Returns:
        状态，CalendarQueryResult，枚举。注意，可能包含代表异常的枚举。
    '''
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

    return calendar.query_date_status(date)


def is_open(market_type, date=None, *, use_cn_mirror_site=False):
    '''
    对 query_date_status 方法的封装，自动处理异常情况。

    Parameters:
        同 query_date_status 方法

    Returns:
        是否为交易日，布尔类型。
    '''
    query_result = query_date_status(market_type, date, use_cn_mirror_site=use_cn_mirror_site)
    if query_result > CalendarQueryResult.Opened:
        raise Exception('calendar query error')

    return query_result == CalendarQueryResult.Opened
