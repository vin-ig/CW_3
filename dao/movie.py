from sqlalchemy import desc

from dao.model.movie import Movie
from dao.model.director import Director
from dao.model.genre import Genre
from constants import QUERY
from dao.model.user import User
from utils import get_pagination


class MovieDAO:
	def __init__(self, session):
		self.session = session

	def get_one(self, uid):
		"""Возвращает один фильм"""
		return self.session.query(Movie).get(uid)

	def get_all(self, page, status):
		"""Возвращает все фильмы"""
		select = self.session.query(Movie)

		offs, lim = get_pagination(Movie, page)

		if status == 'new':
			select = select.order_by(desc(Movie.year))

		return select.limit(lim).offset(offs).all()

	def get_favourites(self, user_id):
		select = self.session.query(Movie)
		return select.all()
