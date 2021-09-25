# py -m python_api.test_api
import unittest
from . import exchange_calendar


class TestApi(unittest.TestCase):

    def setUp(self):
        return

    def tearDown(self):
        return

    def test_query(self):
        query_result = exchange_calendar.query_date_status('cn', '20210921', use_cn_mirror_site=True)
        print(query_result)
        query_result = exchange_calendar.query_date_status('cn', '20210922', use_cn_mirror_site=True)
        print(query_result)
        query_result = exchange_calendar.query_date_status('cn', use_cn_mirror_site=True)
        print(query_result)

    def test_is_open(self):
        opened = exchange_calendar.is_open('cn', '20210921', use_cn_mirror_site=True)
        print(opened)
        opened = exchange_calendar.is_open('cn', use_cn_mirror_site=True)
        print(opened)


if __name__ == '__main__':
    unittest.main()
