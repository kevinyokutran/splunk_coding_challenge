import unittest
import requests
import json


class TestURL(unittest.TestCase):

    url = 'https://splunk.mocklab.io/movies'
    drop_box_url = "https://api.dropboxapi.com/2/files/get_metadata"
    max_genre_ids = 400
    max_genre_ids_count = 7

    # def test_print(self):
    #     """
    #     SPL-005:
    #     There is at least one movie in the database whose title has a palindrome in it.
    #     """
    #     r = self._get_movies(movie='batman')
    #     print(self._validate_drop_box_link('https://www.dropbox.com/s/8i8v4ak8tnp03w4/'))

    def test_spl_004(self):
        """
        SPL-004:
        The number of movies whose sum of "genre_ids" < 400 should be no more than 7.
        """
        r = self._get_movies(movie='batman')
        count = 0
        for movie in r.json()['results']:
            if sum(movie['genre_ids']) > self.max_genre_ids:
                count += 1
        self.assertTrue(count <= self.max_genre_ids_count, 'Exceeded max count')

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

    def _validate_drop_box_link(self, url):
        headers = {
            "Authorization": "Bearer null",
            "Content-Type": "application/json",
            "Dropbox-Api-Select-User": ""
        }
        data = {
            "path": url
        }
        if url is None:
            return True
        else:
            r = requests.post(self.drop_box_url, headers=headers, data=json.dumps(data))
            return r.status_code

    @staticmethod
    def _is_palindrome(s):
        return str(s) == str(s)[::-1]


if __name__ == '__main__':
    unittest.main()

# curl -X GET https://splunk.mocklab.io/movies?q=batman -H "Accept: application/json"