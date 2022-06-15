from sqlalchemy import desc

from dao.model.movie import Movie
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
