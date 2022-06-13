from sqlalchemy import desc

from dao.model.favourites import Favourites
from dao.model.director import Director
from dao.model.genre import Genre
from constants import QUERY
from utils import get_pagination


class FavouritesDAO:
	def __init__(self, session):
		self.session = session

	def get_one(self, uid):
		"""Возвращает один фильм"""
		return self.session.query(Favourites).get(uid)

	def get_all(self, page, status):
		"""Возвращает все фильмы"""
		select = self.session.query(Favourites)

		offs, lim = get_pagination(Favourites, page)

		if status == 'new':
			select = select.order_by(desc(Favourites.year))

		return select.limit(lim).offset(offs).all()
