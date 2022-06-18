from flask_restx import Namespace, Resource
from flask import request

from implemented import movie_service
from dao.model.movie import MovieSchema

movie_ns = Namespace('movies')

movie_s = MovieSchema()
movies_s = MovieSchema(many=True)


@movie_ns.route('/')
class MoviesView(Resource):
	@movie_ns.response(200, description='Все фильмы')
	def get(self):
		"""Выводит все фильмы"""
		page = request.args.get('page')
		status = request.args.get('status')
		movies = movie_service.get_all(page, status)

		return movies_s.dump(movies), 200


@movie_ns.doc(params={'uid': 'Movie ID'})
@movie_ns.route('/<int:uid>/')
class MovieView(Resource):
	@movie_ns.response(404, 'Movie not found')
	def get(self, uid):
		"""Выводит один фильм"""
		try:
			movie = movie_service.get_one(uid)
			return movie_s.dump(movie), 200
		except AttributeError:
			return 'Нет фильма с таким ID', 404
