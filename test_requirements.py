import unittest
from BaseTest import BaseTest


class TestRequirements(BaseTest):

    max_genre_ids = 400
    max_genre_ids_count = 7
    expected_similar_count = 2

    def setUp(self):
        self.response = self.get_movies(movie=self.default_movie)

    def tearDown(self):
        pass

    def test_spl_001(self):
        """
        SPL-001:
        No two movies should have the same image
        """
        images = []
        for movie in self.response.json()['results']:
            if movie['poster_path'] in images:
                self.assertTrue(
                    False,
                    'Duplicate image found, ' + movie['poster_path'])
            images.append(movie['poster_path'])

    def test_spl_002(self):
        """
        SPL-002:
        All poster_path links must be valid. poster_path
        link of null is also acceptable
        """
        for movie in self.response.json()['results']:
            self.assertTrue(
                self.is_drop_box_link_valid(movie['poster_path']),
                "Invalid poster_path: " + movie['poster_path'])

    def test_spl_003(self):
        """
        SPL-003:
        Sorting requirement.
        Rule #1 Movies with genre_ids == null should
        be first in response. Rule #2, if multiple movies
        have genre_ids == null, then sort by id (ascending).
        For movies that have non-null genre_ids, results
        should be sorted by id (ascending)
        """
        prev = None
        for movie in self.response.json()['results']:
            if prev is not None:
                if movie['genre_ids'] is None and prev['genre_ids'] is None:
                    self.assertTrue(
                        movie['id'] > prev['id'],
                        'SPL-003 Rule #2 violated, movies with' +
                        'null genre ids are not sorted by id')
                elif movie['genre_ids'] is not None and prev['genre_ids'] is not None:
                    self.assertTrue(
                        movie['id'] > prev['id'],
                        'SPL-003 Rule #2 violated, movies with non null' +
                        'genre ids are not sorted by id')
                else:
                    self.assertTrue(
                        False,
                        'SPL-003 Rule #1 violated. Null genre ids are not first')
            prev = movie

    def test_spl_004(self):
        """
        SPL-004:
        The number of movies whose sum of "genre_ids" < 400
        should be no more than 7.
        """
        count = 0
        for movie in self.response.json()['results']:
            if sum(movie['genre_ids']) > self.max_genre_ids:
                count += 1
        self.assertTrue(count <= self.max_genre_ids_count,
                        'Exceeded max count')

    def test_spl_005(self):
        """
        SPL-005:
        There is at least one movie in the database whose
        title has a palindrome in it.
        """
        count = 0
        for movie in self.response.json()['results']:
            for word in movie['title'].split():
                if self.is_palindrome(word):
                    count += 1
        self.assertTrue(count > 0,
                        'No palindromes in any titles')

    def test_spl_006(self):
        """
        SPL-006:
        There are at least two movies in the database whose
        title contain the title of another movie.
        """
        count = 0
        for movie1 in self.response.json()['results']:
            for movie2 in self.response.json()['results']:
                if (movie1['title'] != movie2['title'] and
                    (movie1['title'] in movie2['title'] or
                     movie2['title'] in movie1['title'])):
                    count += 1
        self.assertTrue(count >= self.expected_similar_count,
                        'Not enough similar titles')


if __name__ == '__main__':
    unittest.main()