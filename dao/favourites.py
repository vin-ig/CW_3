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

	def get_all(self):
		"""Возвращает все фильмы"""
		# select = self.session.query(Favourites, Movie.id.label('movie_id')).outerjoin(Movie)
		select = self.session.query(Movie).filter(Movie.id == Favourites.movie_id, 1 == Favourites.user_id)
		# select = select.join(Movie)


		# offs, lim = get_pagination(Favourites, page)
		# return select.limit(lim).offset(offs).all()

		return select.all()
