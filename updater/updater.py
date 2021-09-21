''' 更新 data 目录下的 json 文件
'''
from .exchange_calendar import ExchangeCalendar
from . import json_helper


def update_cn_json():
    calendar = ExchangeCalendar('cn')
    record_list = calendar.get_value()
    json_helper.save_to_file(record_list, './data/cn.json')


def update():
    update_cn_json()
