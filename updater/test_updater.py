# py -m updater.test_updater
import unittest
from . import updater


class TestUpdater(unittest.TestCase):

    def setUp(self):
        return

    def tearDown(self):
        return

    def test(self):
        updater.update_cn_json()


if __name__ == '__main__':
    unittest.main()
