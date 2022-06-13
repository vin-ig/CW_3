from flask import request
from flask_restx import Resource, Namespace

from dao.model.genre import GenreSchema
from implemented import genre_service

genre_ns = Namespace('genres')

genre_s = GenreSchema()
genres_s = GenreSchema(many=True)


@genre_ns.route('/')
class GenresView(Resource):
	def get(self):
		"""Выводит всех режиссеров"""
		page = request.args.get('page')
		genres = genre_service.get_all(page)
		return genres_s.dump(genres), 200


@genre_ns.route('/<int:uid>/')
class GenreView(Resource):
	def get(self, uid):
		"""Выводит одого режиссера"""
		genre = genre_service.get_one(uid)
		if genre:
			return genre_s.dump(genre), 200
		else:
			return 'Нет режиссера с таким ID', 404
