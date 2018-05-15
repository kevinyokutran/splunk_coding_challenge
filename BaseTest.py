import unittest
import requests
import json
from requests.exceptions import MissingSchema


class BaseTest(unittest.TestCase):

    splunk_url = 'https://splunk.mocklab.io/movies'
    default_movie = 'batman'

    def get_movies(self, movie, count=0):
        params = {'q': movie, 'count': count, }
        headers = {'accept': 'application/json'}
        return requests.get(self.splunk_url,
                            params=params,
                            headers=headers)

    def post_movie(self, name, description):
        payload = {'name': name, 'description': description}
        headers = {'Content-Type': 'application/json'}
        return requests.post(self.splunk_url,
                             headers=headers,
                             data=json.dumps(payload))

    @staticmethod
    def is_drop_box_link_valid(url):
        headers = {
            "Accept": "application/json",
        }
        if url is None:
            return True
        else:
            try:
                r = requests.get(url, headers=headers)
                return r.status_code == 200
            except MissingSchema:
                return False

    @staticmethod
    def is_palindrome(s):
        return str(s) == str(s)[::-1]


if __name__ == '__main__':
    unittest.main()