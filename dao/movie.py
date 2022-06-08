from dao.model.movie import Movie
from dao.model.director import Director
from dao.model.genre import Genre
from constants import QUERY
from utils import get_pagination


class MovieDAO:
	def __init__(self, session):
		self.session = session

	def get_one(self, uid):
		"""Возвращает один фильм (для использования в других методах)"""
		return self.session.query(Movie).get(uid)

	def get_one_join(self, uid):
		"""Возвращает один фильм (для вьюшек)"""
		movie = self.session.query(Movie).get(uid)

		if movie.director_id and movie.genre_id:
			query_ = Director.name.label('director'), Genre.name.label('genre')
			return self.session.query(*QUERY, *query_).join(Director).join(Genre).filter(Movie.id == uid).first()
		elif movie.director_id:
			query_ = Director.name.label('director')
			return self.session.query(*QUERY, query_).filter(Movie.id == uid).first()
		elif movie.genre_id:
			query_ = Genre.name.label('genre')
			return self.session.query(*QUERY, query_).join(Genre).filter(Movie.id == uid).first()
		else:
			return movie

	def get_all(self, page, status):
		"""Возвращает все фильмы"""
		query_ = Director.name.label('director'), Genre.name.label('genre')
		select = self.session.query(*QUERY, *query_).join(Director).join(Genre)

		offs, lim = get_pagination(Movie, page)

		if status == 'new':
			select = select.order_by(Movie.year)

		return select.limit(lim).offset(offs).all()

	def create(self, data):
		"""Добавляет новый фильм"""
		movie = Movie(**data)
		self.session.add(movie)
		self.session.commit()
		return movie

	def update(self, movie):
		"""Обновляет фильм"""
		self.session.add(movie)
		self.session.commit()
		return movie

	def delete(self, uid):
		"""Удаляет фильм"""
		movie = self.get_one(uid)
		self.session.delete(movie)
		self.session.commit()
