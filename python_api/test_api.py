# py -m python_api.test_api
import unittest
from . import exchange_calendar
from . import app_config


class TestApi(unittest.TestCase):

    def setUp(self):
        return

    def tearDown(self):
        return

    @unittest.skip('')
    def test_query(self):
        query_result = exchange_calendar.query_date_status('cn', '20210921', use_cn_mirror_site=True)
        print(query_result)
        query_result = exchange_calendar.query_date_status('cn', '20210922', use_cn_mirror_site=True)
        print(query_result)
        query_result = exchange_calendar.query_date_status('cn', use_cn_mirror_site=True)
        print(query_result)

    @unittest.skip('')
    def test_is_open(self):
        opened = exchange_calendar.is_open('cn', '20200101', use_cn_mirror_site=True)
        print(opened)
        opened = exchange_calendar.is_open('cn', use_cn_mirror_site=True)
        print(opened)

    @unittest.skip('')
    def test_config(self):
        redis_server_ip = app_config.get('redis_server_ip')
        self.assertTrue(len(redis_server_ip) > 0)


if __name__ == '__main__':
    unittest.main()
