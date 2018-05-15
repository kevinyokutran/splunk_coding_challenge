import unittest
import random
from BaseTest import BaseTest


class TestAPI(BaseTest):

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
        r = self.get_movies(movie=self.default_movie)
        self.assertTrue(r.status_code == 200,
                        'Expected 200, received ' + str(r.status_code))
        self.assertTrue(len(r.json()['results']) > 0,
                        'No movies found')

    def test_get_valid_movies_with_count(self):
        """
        Get batman movies that are expected to exist, using count
        Assert: HTTP 200, # of movies returned == count specified
        """
        count = 3
        r = self.get_movies(movie=self.default_movie, count=count)
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
        r = self.get_movies(movie='invalid_movie')
        self.assertTrue(r.status_code == 404,
                        'Expected 404, received ' + str(r.status_code))

    def test_post_movie(self):
        """
        Make POST request to API and verify it was correctly added
        Assert: HTTP 200 on POST, movie exists in GET request
        TODO: Remove random element once API supports deletion of movies.
        """
        name = "Movie" + str(random.randint(0, 1000000))
        desc = str(random.randint(0, 1000000))
        r = self.post_movie(name=name, description=desc)
        self.assertTrue(r.status_code == 200,
                        'Expected 200, received ' + str(r.status_code))
        r = self.get_movies(movie=name)
        found = False
        for movie in r.json()['results']:
            if movie['title'] == name:
                found = True
        self.assertTrue(found, 'Posted movie not found (' + name + ')')

    def test_post_duplicate_movie(self):
        """
        Make duplicate POST request to API and verify it was correctly added
        Assert: HTTP 200 on POST, movie exists in GET request
        TODO: Remove random element once API supports deletion of movies.
        TODO: Verify expected behaviour, currently returns success message
        """
        name = "Movie" + str(random.randint(0, 1000000))
        desc = str(random.randint(0, 1000000))
        r = self.post_movie(name=name, description=desc)
        self.assertTrue(r.status_code == 200,
                        'Expected 200, received ' + str(r.status_code))
        r = self.post_movie(name=name, description=desc)
        self.assertTrue(r.status_code == 200,
                        'Expected 200, received ' + str(r.status_code))

    def test_post_long_movie(self):
        """
        Make POST request to API with long strings
        Assert: HTTP 200 on POST
        """
        r = self.post_movie(name="LongName"*100000, description="LongDesc"*100000)
        self.assertTrue(r.status_code == 200,
                        'Expected 200, received ' + str(r.status_code))

    def test_post_long_movie(self):
        """
        Make POST request to API with null strings
        Assert: HTTP 200 on POST
        """
        r = self.post_movie(name="", description="")
        self.assertTrue(r.status_code == 200,
                        'Expected 200, received ' + str(r.status_code))


if __name__ == '__main__':
    unittest.main()