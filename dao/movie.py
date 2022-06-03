from app.dao.model.movie import Movie
from app.dao.model.director import Director
from app.dao.model.genre import Genre
from app.constants import QUERY


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

	def get_all(self, filter, value):
		"""Возвращает все фильмы"""
		query_ = Director.name.label('director'), Genre.name.label('genre')
		select = self.session.query(*QUERY, *query_).join(Director).join(Genre)

		# Делаем подборку по фильтрам
		if filter == 'year':
			return select.filter(Movie.year == value).all()
		elif filter == 'director':
			return select.filter(Movie.director_id == value).all()
		elif filter == 'genre':
			return select.filter(Movie.genre_id == value).all()

		return select.all()

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
