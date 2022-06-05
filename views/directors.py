from flask import request
from flask_restx import Resource, Namespace

from dao.model.director import DirectorSchema
from implemented import director_service
from utils import auth_required, admin_required

director_ns = Namespace('directors')

director_s = DirectorSchema()
directors_s = DirectorSchema(many=True)


@director_ns.route('/')
class DirectorsView(Resource):
	# @auth_required
	def get(self):
		"""Выводит всех режиссеров"""
		directors = director_service.get_all()
		return directors_s.dump(directors), 200

	# @admin_required
	def post(self):
		data = request.json
		director = director_service.create(data)
		return "", 201, {"location": f"/movies/{director.id}"}


@director_ns.route('/<int:uid>')
class DirectorView(Resource):
	# @auth_required
	def get(self, uid):
		"""Выводит одого режиссера"""
		director = director_service.get_one(uid)
		if director:
			return director_s.dump(director), 200
		else:
			return 'Нет режиссера с таким ID', 404

	# @admin_required
	def put(self, uid):
		req_json = request.json
		if "id" not in req_json:
			req_json["id"] = uid
		director_service.update(req_json)
		return "", 204

	# @admin_required
	def delete(self, uid):
		director_service.delete(uid)
		return "", 204
