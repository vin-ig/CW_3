from flask import request
from flask_restx import Namespace, Resource

from constants import USER_KEYS
from implemented import user_service
from utils import check_keys

user_ns = Namespace('users')


@user_ns.route('/')
class UsersVIew(Resource):
	def post(self):
		data = request.json
		try:
			check_keys(data, USER_KEYS)
			user = user_service.create(data)
			return 'User successfully created', 201, {"location": f"/movies/{user.id}"}
		except Exception as error:
			return f'{error}', 200
