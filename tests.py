import unittest
import requests
import json


class TestURL(unittest.TestCase):

    url = 'https://splunk.mocklab.io/movies'


    def test_spl_005(self):
        """
        SPL-005:
        There is at least one movie in the database whose title has a palindrome in it.
        """
        r = self._get_movies(movie='batman')
        count = 0
        for movie in r.json()['results']:
            for word in movie['title'].split():
                if self._is_palindrome(word):
                    count += 1
        self.assertTrue(count > 0, 'No palindromes in any titles')

    def _get_movies(self, movie, count=0):
        params = {'q': movie}
        headers = {'accept': 'application/json'}
        return requests.get(self.url, params=params, headers=headers)

    def _post_movies(self, movie):
        params = {'q': movie}
        headers = {'accept': 'application/json'}
        return requests.post(self.url, data=json.dumps(params))

    @staticmethod
    def _is_palindrome(s):
        return str(s) == str(s)[::-1]


if __name__ == '__main__':
    unittest.main()

# curl -X GET https://splunk.mocklab.io/movies?q=batman -H "Accept: application/json"