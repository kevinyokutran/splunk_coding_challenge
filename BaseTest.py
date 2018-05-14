import unittest
import requests
import json


class BaseTest(unittest.TestCase):

    url = 'https://splunk.mocklab.io/movies'
    drop_box_url = "https://api.dropboxapi.com/2/files/get_metadata"

    def get_movies(self, movie, count=0):
        params = {'q': movie, 'count': count, }
        headers = {'accept': 'application/json'}
        return requests.get(self.url, params=params, headers=headers)

    def post_movie(self, name, description):
        payload = {'name': name, 'description': description}
        headers = {'Content-Type': 'application/json'}
        return requests.post(self.url, headers=headers, data=json.dumps(payload))

    @staticmethod
    def is_palindrome(s):
        return str(s) == str(s)[::-1]


if __name__ == '__main__':
    unittest.main()