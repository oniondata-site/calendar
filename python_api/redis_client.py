from redis import StrictRedis
from . import app_config


def create_redis_client():
    redis_server_ip = app_config.get('redis_server_ip')
    redis_server_port = app_config.get('redis_server_port')
    redis_server_password = app_config.get('redis_server_password')
    # 没有配置，跳过
    if not redis_server_ip or not redis_server_password:
        return None

    client = StrictRedis(host=redis_server_ip, port=redis_server_port, db=1, password=redis_server_password, decode_responses=True)
    return client
