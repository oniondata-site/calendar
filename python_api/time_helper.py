import copy
import time
from datetime import datetime, timedelta


INITIAL_STOCK_DATE = '20100101'
INITIAL_STOCK_WEEKLY_DATE = '20100108'

HOUR_IN_SECOND = 60 * 60
DAY_IN_SECOND = 24 * 60 * 60


def get_today_date_text():
    # 20150101
    return datetime.today().strftime('%Y%m%d')
    # 2015-01-01
    # return str(datetime.today().date())


def shift_date_text(date, offset):
    date = datetime.strptime(date, '%Y%m%d')
    date_offset = date + timedelta(days=offset)
    return date_offset.strftime('%Y%m%d')


def get_stock_range_date_text():
    return INITIAL_STOCK_DATE, get_today_date_text()


def timestamp_to_date_text(timestamp):
    date = datetime.fromtimestamp(timestamp).date()
    return date.strftime('%Y%m%d')


def split_timestamp_date_and_time(timestamp):
    ''' 输出 date_text eg: 20170101
             day_time，精确到秒
    '''
    date = datetime.fromtimestamp(timestamp)
    date_text = date.strftime('%Y%m%d')

    timetuple = date.timetuple()
    day_time = timetuple.tm_hour * 60 * 60 + timetuple.tm_min * 60 + timetuple.tm_sec
    return date_text, day_time


def date_text_to_timestamp(date_text):
    date = datetime.strptime(date_text, '%Y%m%d')
    return time.mktime(date.timetuple())


def date_text_to_weekday(date_text):
    date = datetime.strptime(date_text, '%Y%m%d')
    return date.weekday()


def date_text_to_month(date_text):
    date = datetime.strptime(date_text, '%Y%m%d')
    return date.month


def date_text_delta(date_text_1, date_text_2=None):
    date_1 = datetime.strptime(date_text_1, '%Y%m%d')
    if date_text_2 is None:
        date_2 = datetime.now()
    else:
        date_2 = datetime.strptime(date_text_2, '%Y%m%d')

    delta = date_1 - date_2
    return abs(delta.days)


def date_text_is_same_week(date_text_1, date_text_2):
    if date_text_1 < date_text_2:
        date_1 = datetime.strptime(date_text_1, '%Y%m%d')
        date_2 = datetime.strptime(date_text_2, '%Y%m%d')
    else:
        date_2 = datetime.strptime(date_text_1, '%Y%m%d')
        date_1 = datetime.strptime(date_text_2, '%Y%m%d')

    delta = date_2 - date_1
    if delta.days > 6:
        return False
    elif delta.days == 6:
        return date_1.weekday() != date_2.weekday()
    else:
        return date_1.weekday() <= date_2.weekday()


def today_to_timestamp(hour, minute=0, second=0):
    localtime_sequence = list(time.localtime())
    localtime_sequence[3] = hour  # tm_hour
    localtime_sequence[4] = minute
    localtime_sequence[5] = second
    next_localtime = time.struct_time(localtime_sequence)

    next_timestamp = time.mktime(next_localtime)

    return next_timestamp


def filter_next_time(hms_list):
    candicate_list = copy.copy(hms_list)

    for i in range(len(hms_list)):
        hms = hms_list[i]
        tomorrow_hms = [hms[0] + 24, hms[1], hms[2]]

        candicate_list.append(tomorrow_hms)

    now_time = time.time()
    for hms in candicate_list:
        ts = today_to_timestamp(*hms)
        if now_time < ts:
            return ts


def timestamp_to_ch_second_in_day(timestamp):
    return (timestamp + 8 * HOUR_IN_SECOND) % (24 * HOUR_IN_SECOND)


if __name__ == '__main__':
    date_text = timestamp_to_date_text(time.time())
    print(date_text)
    print(get_today_date_text())
    print(split_timestamp_date_and_time(time.time()))
    print(date_text_to_timestamp('20150101'))
