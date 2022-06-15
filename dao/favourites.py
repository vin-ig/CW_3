from dao.model.favourites import Favourites
from dao.model.movie import Movie


class FavouritesDAO:
	def __init__(self, session):
		self.session = session

	def get_all(self, uid):
		"""Возвращает избранные фильмы"""
		return self.session.query(Movie).\
			filter(Movie.id == Favourites.movie_id, Favourites.user_id == uid).\
			all()

	def add(self, data):
		"""Добавляет фильм в избранное"""
		self.session.add(Favourites(**data))
		self.session.commit()

	def delete(self, movie_id):
		"""Удаляет фильм из избранного"""
		raw = self.session.query(Favourites).filter(Favourites.movie_id == movie_id).one()
		self.session.delete(raw)
		self.session.commit()
