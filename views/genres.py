from flask import request
from flask_restx import Resource, Namespace

from dao.model.genre import GenreSchema
from implemented import genre_service
from utils import auth_required, admin_required

genre_ns = Namespace('genres')

genre_s = GenreSchema()
genres_s = GenreSchema(many=True)


@genre_ns.route('/')
class GenresView(Resource):
	# @auth_required
	def get(self):
		"""Выводит всех режиссеров"""
		page = request.args.get('page')
		genres = genre_service.get_all(page)
		return genres_s.dump(genres), 200

	# @admin_required
	def post(self):
		data = request.json
		genre = genre_service.create(data)
		return "", 201, {"location": f"/movies/{genre.id}"}


@genre_ns.route('/<int:uid>')
class GenreView(Resource):
	# @auth_required
	def get(self, uid):
		"""Выводит одого режиссера"""
		genre = genre_service.get_one(uid)
		if genre:
			return genre_s.dump(genre), 200
		else:
			return 'Нет режиссера с таким ID', 404

	# @admin_required
	def put(self, uid):
		req_json = request.json
		if "id" not in req_json:
			req_json["id"] = uid
		genre_service.update(req_json)
		return "", 204

	# @admin_required
	def delete(self, uid):
		genre_service.delete(uid)
		return "", 204
