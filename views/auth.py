import datetime

import jwt
from flask import request, abort
from flask_restx import Namespace, Resource

from constants import SECRET, ALGO, TOKEN_KEYS
from dao.model.user import UserSchema
from implemented import user_service
from utils import check_keys, generate_jwt

auth_ns = Namespace('auth')


@auth_ns.route('/')
class AuthVIew(Resource):
	def post(self):
		data = request.json
		username = data.get('username')
		password = data.get('password')

		try:
			user = user_service.get_one(username)
			user_service.check_password(user.username, password)
		except Exception:
			abort(401)

		user_dict = UserSchema().dump(user)
		return generate_jwt(user_dict), 201

	def put(self):
		token = request.json.get('refresh_token')

		try:
			decode_token = jwt.decode(token, SECRET, ALGO)
			time = datetime.datetime.fromtimestamp(decode_token['exp'])
			check_keys(decode_token, TOKEN_KEYS)
			if datetime.datetime.utcnow() > time:
				raise Exception('Expired token')
			return generate_jwt(decode_token), 201
		except Exception as error:
			return f'{error}', 200
