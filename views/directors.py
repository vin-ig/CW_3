from flask import request
from flask_restx import Resource, Namespace

from dao.model.director import DirectorSchema
from implemented import director_service
from utils import convert_schema_to_flask_model

director_ns = Namespace('directors')

director_s = DirectorSchema()
directors_s = DirectorSchema(many=True)

flask_schema = convert_schema_to_flask_model(directors_s)
output_model = director_ns.model('Directors', flask_schema)


@director_ns.route('/')
class DirectorsView(Resource):
	@director_ns.response(200, description='Режиссеры', model=output_model)
	def get(self):
		"""Выводит всех режиссеров"""
		page = request.args.get('page')
		directors = director_service.get_all(page)
		return directors_s.dump(directors), 200


@director_ns.doc(params={'uid': 'Director ID'})
@director_ns.route('/<int:uid>/')
class DirectorView(Resource):
	@director_ns.response(200, description='Выбранный режиссер', model=output_model)
	def get(self, uid):
		"""Выводит одного режиссера"""
		director = director_service.get_one(uid)
		if director:
			return director_s.dump(director), 200
		else:
			return 'Нет режиссера с таким ID', 404
