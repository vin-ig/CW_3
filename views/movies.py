from flask_restx import Namespace, Resource
from flask import request, jsonify
from sqlalchemy.orm import exc

from constants import MOVIE_KEYS
from implemented import movie_service
from dao.model.movie import MovieSchema
from utils import check_keys

movie_ns = Namespace('movies')

movie_s = MovieSchema()
movies_s = MovieSchema(many=True)


@movie_ns.route('/')
class MoviesView(Resource):
	def get(self):
		"""Выводит все фильмы"""
		page = request.args.get('page')
		status = request.args.get('status')
		movies = movie_service.get_all(page, status)

		return movies_s.dump(movies), 200

	def post(self):
		"""Добавляет новый фильм"""
		data = request.json
		if not check_keys(data, MOVIE_KEYS):
			return 'Переданы неверные ключи', 200
		new_movie = movie_service.create(data)
		response = jsonify()
		response.status_code = 201
		response.headers['location'] = f'movies/{new_movie.id}'
		return response


@movie_ns.route('/<int:uid>/')
class MovieView(Resource):
	def get(self, uid):
		"""Выводит один фильм"""
		try:
			movie = movie_service.get_one(uid)
			return movie_s.dump(movie), 200
		except AttributeError:
			return 'Нет фильма с таким ID', 404

	def put(self, uid):
		"""Выполняет полное обновление полей фильма"""
		try:
			data = request.json
			if not check_keys(data, MOVIE_KEYS):
				return 'Переданы неверные ключи', 200

			movie_service.update(data, uid)
			return 'Данные фильма обновлены', 200

		except AttributeError:
			return 'Нет фильма с таким ID', 404

	def patch(self, uid):
		"""Выполняет частичное обновление полей фильма"""
		try:
			data = request.json
			if not check_keys(data, MOVIE_KEYS):
				return 'Переданы неверные ключи', 200

			movie_service.update(data, uid)
			return 'Данные фильма обновлены', 200

		except AttributeError:
			return 'Нет фильма с таким ID', 404

	def delete(self, uid):
		"""Удаляет фильм"""
		try:
			movie_service.delete(uid)
			return 'Фильм удален', 200
		except (AttributeError, exc.UnmappedInstanceError):
			return 'Нет фильма с таким ID', 404
