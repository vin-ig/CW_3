import datetime

import jwt
from flask import request, abort
from flask_restx import Namespace, Resource

from constants import SECRET, ALGO, TOKEN_KEYS, USER_KEYS
from dao.model.user import UserSchema
from implemented import user_service, auth_service
from utils import check_keys


auth_ns = Namespace('auth')


@auth_ns.route('/register/')
class AuthRegisterView(Resource):
	def post(self):
		"""Регистрация нового пользователя"""
		data = request.json
		try:
			check_keys(data, USER_KEYS)
			user = user_service.create(data)
			return 'User successfully created', 201, {"location": f"/auth/register/{user.id}"}
		except Exception as error:
			return f'{error}', 200


@auth_ns.route('/login/')
class AuthLoginVIew(Resource):
	def post(self):
		"""Авторизация пользователя"""
		email = request.json.get('email')
		password = request.json.get('password')

		try:
			user = user_service.get_one(email)
			user_service.check_password(user.email, password)
			# user_service.__compare_password(user.password, password)
		except Exception:
			abort(401)

		user_dict = UserSchema().dump(user)
		return auth_service.generate_jwt(user_dict), 201

	def put(self):
		"""Генерация новых токенов"""
		# access_token = request.json.get('access_token')
		token = request.json.get('refresh_token')

		try:
			decode_token = jwt.decode(token, SECRET, ALGO)
			time = datetime.datetime.fromtimestamp(decode_token['exp'])
			check_keys(decode_token, TOKEN_KEYS)
			if datetime.datetime.utcnow() > time:
				raise Exception('Expired token')
			return auth_service.generate_jwt(decode_token), 201
		except Exception as error:
			return f'{error}', 200
