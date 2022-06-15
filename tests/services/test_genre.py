import pytest
from unittest.mock import MagicMock

from dao.model.genre import Genre
from service.genre import GenreService
from dao.genre import GenreDAO


@pytest.fixture
def genre_dao():
	genre = GenreDAO(None)

	g1 = Genre(id=1, name='musical')
	g2 = Genre(id=2, name='comedy')
	g3 = Genre(id=3, name='thriller')

	genre.get_one = MagicMock(return_value=g2)
	genre.get_all = MagicMock(return_value=[g1, g2, g3])

	return genre


class TestGenreService:
	@pytest.fixture(autouse=True)
	def genre_service(self, genre_dao):
		self.genre_service = GenreService(dao=genre_dao)

	def test_get_one(self):
		genre = self.genre_service.get_one(2)
		assert genre is not None
		assert genre.id is not None

	def test_get_all(self):
		genres = self.genre_service.get_all(2)
		assert len(genres) != 0
