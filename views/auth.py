import datetime

import jwt
from flask import request, abort
from flask_restx import Namespace, Resource, fields

from constants import SECRET, ALGO, TOKEN_KEYS, USER_KEYS
from dao.model.user import UserSchema
from implemented import user_service, auth_service
from utils import check_keys


auth_ns = Namespace('auth')

input_model = auth_ns.model(
	'AuthRegisterRequest',
	{
		'email': fields.String,
		'password': fields.String
	}
)
input_tokens_model = auth_ns.model(
	'TokenRequest',
	{
		'access_token': fields.String,
		'refresh_token': fields.String,
	}
)
output_model = auth_ns.model(
	'TokenResponse',
	{
		'access_token': fields.String,
		'refresh_token': fields.String,
	}
)


@auth_ns.route('/register/')
class AuthRegisterView(Resource):
	@auth_ns.expect(input_model)
	@auth_ns.response(201, description='Пользователь зарегистрирован')
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
	@auth_ns.response(200, description='Токены для авторизации', model=output_model)
	def post(self):
		"""Авторизация пользователя"""
		email = request.json.get('email')
		password = request.json.get('password')

		try:
			user = user_service.get_one(email)
			user_service.check_password(user.email, password)
		except Exception:
			abort(401)

		user_dict = UserSchema().dump(user)
		return auth_service.generate_jwt(user_dict), 201

	@auth_ns.expect(input_tokens_model)
	@auth_ns.response(200, description='Токены для авторизации', model=output_model)
	def put(self):
		"""Генерация новых токенов"""
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
