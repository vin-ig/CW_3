import pytest

from dao.movie import MovieDAO
from dao.model.movie import Movie


class TestMovieDAO:
	@pytest.fixture(autouse=True)
	def dao(self, db):
		self.dao = MovieDAO(db.session)

	@pytest.fixture
	def movie_1(self, db):
		m = Movie(title="ff", description="ff", trailer="ff", year=13, rating=13, genre_id=13, director_id=13)
		db.session.add(m)
		db.session.commit()
		return m

	@pytest.fixture
	def movie_2(self, db):
		m = Movie(title="dd", description="dd", trailer="dd", year=13, rating=13, genre_id=13, director_id=13)
		db.session.add(m)
		db.session.commit()
		return m

	def test_get_movie_by_id(self, movie_1):
		assert self.dao.get_one(movie_1.id) == movie_1

	def test_get_movie_by_id_not_found(self):
		assert self.dao.get_one(1) is None

	def test_get_all_movies(self, movie_1, movie_2):
		assert self.dao.get_all(1, 'new') == [movie_1, movie_2]
