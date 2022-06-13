import jwt
from flask import request
from flask_restx import Namespace, Resource

from constants import USER_KEYS, SECRET, ALGO
from dao.model.user import UserSchema
from implemented import user_service
from utils import check_keys, auth_required

user_ns = Namespace('user')
user_s = UserSchema()


@user_ns.route('/')
class UsersVIew(Resource):
	@auth_required
	def get(self, email):
		user_token = request.headers.get('Authorization').split()[-1]
		decode_data = jwt.decode(user_token, SECRET, ALGO)
		user = user_service.get_one(decode_data.get('email'))
		print(email)
		if user:
			return user_s.dump(user), 200
		else:
			return '', 404

	# @auth_required
	def patch(self):
		"""Выполняет частичное обновление данных пользователя"""
		user_token = request.headers.get('Authorization').split()[-1]
		decode_data = jwt.decode(user_token, SECRET, ALGO)
		user = user_service.get_one(decode_data.get('email'))
		# print(user.email)

		try:
			data = request.json
			# if not check_keys(data, USER_KEYS):
			# 	return 'Переданы неверные ключи', 200

			user_service.update(data, user.email)
			return 'Данные пользователя обновлены', 200

		except AttributeError:
			return 'Нет пользователя с таким ID', 404


@user_ns.route('/password/')
class UserChangePassword(Resource):
	# @auth_required
	def put(self):
		user_token = request.headers.get('Authorization').split()[-1]
		decode_data = jwt.decode(user_token, SECRET, ALGO)
		email = decode_data.get('email')
		user = user_service.get_one(decode_data.get('email'))

		old_password = request.json.get('old_password')
		new_password = request.json.get('new_password')

		user_service.change_password(user.email, old_password, new_password)

		return '', 200
