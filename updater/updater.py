''' 更新 data 目录下的 json 文件
'''
from .exchange_calendar import ExchangeCalendar
from . import json_helper
from python_api.redis_client import create_redis_client


def update_cn_json():
    calendar = ExchangeCalendar('cn')
    record_list = calendar.get_value()
    json_helper.save_to_file(record_list, './data/cn.json')


def save_to_redis():
    client = create_redis_client()
    if client is None:
        return

    with open('./data/cn.json', encoding='utf8') as f:
        text = f.read()
    client.hset('calendar', 'cn.json', text)


def update():
    update_cn_json()
    save_to_redis()
