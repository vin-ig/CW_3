import jwt
from flask import request
from flask_restx import Namespace, Resource

from constants import USER_KEYS, SECRET, ALGO
from dao.model.user import UserSchema
from implemented import user_service, auth_service
from utils import check_keys

user_ns = Namespace('user')
user_s = UserSchema()


@user_ns.route('/')
class UsersVIew(Resource):
	@auth_service.auth_required
	def get(self):
		"""Профиль пользователя"""
		email = auth_service.get_email_from_jwt()
		user = user_service.get_one(email)
		if user:
			return user_s.dump(user), 200
		else:
			return '', 404

	@auth_service.auth_required
	def patch(self):
		"""Выполняет частичное обновление данных пользователя"""
		email = auth_service.get_email_from_jwt()
		user = user_service.get_one(email)

		try:
			data = request.json
			user_service.update(data, user.email)
			return 'Данные пользователя обновлены', 200

		except AttributeError:
			return 'Нет пользователя с таким ID', 404


@user_ns.route('/password/')
class UserChangePassword(Resource):
	@auth_service.auth_required
	def put(self):
		email = auth_service.get_email_from_jwt()
		user = user_service.get_one(email)

		old_password = request.json.get('old_password')
		new_password = request.json.get('new_password')

		user_service.change_password(user.email, old_password, new_password)

		return '', 200
