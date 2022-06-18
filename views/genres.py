from flask import request
from flask_restx import Resource, Namespace

from dao.model.genre import GenreSchema
from implemented import genre_service
from utils import convert_schema_to_flask_model

genre_ns = Namespace('genres')

genre_s = GenreSchema()
genres_s = GenreSchema(many=True)

flask_schema = convert_schema_to_flask_model(genres_s)
output_model = genre_ns.model('Genres', flask_schema)


@genre_ns.route('/')
class GenresView(Resource):
	@genre_ns.response(200, description='Жанры', model=output_model)
	def get(self):
		"""Выводит все жанры"""
		page = request.args.get('page')
		genres = genre_service.get_all(page)
		return genres_s.dump(genres), 200


@genre_ns.doc(params={'uid': 'Genre ID'})
@genre_ns.route('/<int:uid>/')
class GenreView(Resource):
	@genre_ns.response(200, description='Жанр', model=output_model)
	def get(self, uid):
		"""Выводит выбранный жанр"""
		genre = genre_service.get_one(uid)
		if genre:
			return genre_s.dump(genre), 200
		else:
			return 'Нет режиссера с таким ID', 404
