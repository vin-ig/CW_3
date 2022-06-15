from sqlalchemy import desc

from dao.model.favourites import Favourites
from dao.model.director import Director
from dao.model.genre import Genre
from constants import QUERY
from dao.model.movie import Movie
from utils import get_pagination


class FavouritesDAO:
	def __init__(self, session):
		self.session = session

	def get_one(self, uid):
		"""Возвращает один фильм"""
		return self.session.query(Favourites).get(uid)

	def get_all(self, uid):
		"""Возвращает избранные фильмы"""
		return self.session.query(Movie).\
			filter(Movie.id == Favourites.movie_id, Favourites.user_id == uid).\
			all()

	def add(self, data):
		self.session.add(Favourites(**data))
		self.session.commit()

	def delete(self, movie_id):
		raw = self.session.query(Favourites).filter(Favourites.movie_id == movie_id).one()
		self.session.delete(raw)
		self.session.commit()
