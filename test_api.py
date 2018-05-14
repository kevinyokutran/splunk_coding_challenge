import unittest
import requests
import json


class TestAPI(unittest.TestCase):

    url = 'https://splunk.mocklab.io/movies'

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_valid_movies(self):
        """
        Get batman movies that are expected to exist
        Assert: HTTP 200, # of movies returned > 0
        """
        r = self._get_movies(movie='batman')
        self.assertTrue(r.status_code == 200,
                        'Expected 200, received ' + str(r.status_code))
        self.assertTrue(len(r.json()['results']) > 0, 'No movies found')

    def test_get_valid_movies_with_count(self):
        """
        Get batman movies that are expected to exist, using count
        Assert: HTTP 200, # of movies returned > 0
        """
        count = 3
        r = self._get_movies(movie='batman', count=count)
        self.assertTrue(r.status_code == 200,
                        'Expected 200, received ' + str(r.status_code))
        self.assertTrue(len(r.json()['results']) == 3,
                        'Returned more or less movies than expected.' +
                        ' Expected=' + str(count) +
                        ' Returned=' + str(len(r.json()['results']))
                        )

    def test_get_invalid_movies(self):
        """
        Get movies that are not expected to exist
        Assert: HTTP 404
        """
        r = self._get_movies(movie='invalid_movie')
        self.assertTrue(r.status_code == 404,
                        'Expected 404, received ' + str(r.status_code))

    def test_post_movie(self):
        """
        """
        pass

    def _get_movies(self, movie, count=0):
        params = {'q': movie, 'count': count, }
        headers = {'accept': 'application/json'}
        return requests.get(self.url, params=params, headers=headers)

    def _post_movie(self, name, description):
        payload = {'name': name, 'description': description}
        headers = {'content-type': 'application/json'}
        return requests.post(self.url, headers=headers, data=json.dumps(payload))


if __name__ == '__main__':
    unittest.main()

# curl -X GET https://splunk.mocklab.io/movies?q=batman -H "Accept: application/json"