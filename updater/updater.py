''' 更新 data 目录下的 json 文件
'''
from redis import StrictRedis
from .exchange_calendar import ExchangeCalendar
from . import json_helper
from python_api import app_config


def update_cn_json():
    calendar = ExchangeCalendar('cn')
    record_list = calendar.get_value()
    json_helper.save_to_file(record_list, './data/cn.json')


def save_to_redis():
    redis_server_ip = app_config.get('redis_server_ip')
    redis_server_port = app_config.get('redis_server_port')
    redis_server_password = app_config.get('redis_server_password')
    # 没有配置，跳过
    if not redis_server_ip or not redis_server_password:
        return 

    with open('./data/cn.json', encoding='utf8') as f:
        text = f.read()

    client = StrictRedis(host=redis_server_ip, port=redis_server_port, db=1, password=redis_server_password, decode_responses=True)
    client.hset('calendar', 'cn.json', text)


def update():
    update_cn_json()
    save_to_redis()
