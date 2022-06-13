from flask import request
from flask_restx import Resource, Namespace

from dao.model.director import DirectorSchema
from implemented import director_service

director_ns = Namespace('directors')

director_s = DirectorSchema()
directors_s = DirectorSchema(many=True)


@director_ns.route('/')
class DirectorsView(Resource):
	def get(self):
		"""Выводит всех режиссеров"""
		page = request.args.get('page')
		directors = director_service.get_all(page)
		return directors_s.dump(directors), 200


@director_ns.route('/<int:uid>/')
class DirectorView(Resource):
	def get(self, uid):
		"""Выводит одого режиссера"""
		director = director_service.get_one(uid)
		if director:
			return director_s.dump(director), 200
		else:
			return 'Нет режиссера с таким ID', 404
