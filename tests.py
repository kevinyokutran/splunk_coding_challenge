import unittest
import requests


class TestURL(unittest.TestCase):

    URL = 'https://splunk.mocklab.io/movies'

    def test_true(self):
        self.assertTrue()

    def _call_url(self, movie, count=0):
        requests.get(self.url)


if __name__ == '__main__':
    unittest.main()
