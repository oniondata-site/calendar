# py -m updater.test_updater
import unittest
from . import updater


class TestUpdater(unittest.TestCase):

    def setUp(self):
        return

    def tearDown(self):
        return

    @unittest.skip('')
    def test_update_cn_json(self):
        updater.update_cn_json()

    def test_save_to_redis(self):
        updater.save_to_redis()


if __name__ == '__main__':
    unittest.main()
