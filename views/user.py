from flask import request
from flask_restx import Namespace, Resource, fields

from dao.model.user import UserSchema
from implemented import user_service, auth_service
from utils import convert_schema_to_flask_model

user_ns = Namespace('user')
user_s = UserSchema()

input_model = user_ns.model(
	'ChangePassword',
	{
		'old_password': fields.String,
		'new_password': fields.String
	}
)

flask_schema = convert_schema_to_flask_model(user_s)
output_model = user_ns.model('Directors', flask_schema)


@user_ns.route('/')
class UsersVIew(Resource):
	@user_ns.response(200, description='Профиль пользователя', model=output_model)
	@user_ns.doc(description='Профиль пользователя')
	@auth_service.auth_required
	def get(self):
		"""Профиль пользователя"""
		email = auth_service.get_email_from_jwt()
		user = user_service.get_one(email)
		if user:
			return user_s.dump(user), 200
		else:
			return '', 404

	@user_ns.response(200, description='Профиль пользователя', model=output_model)
	@user_ns.doc(description='Изменение имени, фамилии или любимого жанра пользователя')
	@auth_service.auth_required
	def patch(self):
		"""Выполняет частичное обновление данных пользователя"""
		email = auth_service.get_email_from_jwt()
		user = user_service.get_one(email)

		try:
			data = request.json
			user_service.update(data, user.email)
			return user_s.dump(user), 200

		except AttributeError:
			return 'Нет пользователя с таким ID', 404


@user_ns.route('/password/')
class UserChangePassword(Resource):
	@user_ns.expect(input_model)
	@user_ns.response(204, description='Пароль изменен')
	@user_ns.doc(description='Изменение пароля')
	@auth_service.auth_required
	def put(self):
		"""Изменение пароля"""
		email = auth_service.get_email_from_jwt()
		user = user_service.get_one(email)

		old_password = request.json.get('old_password')
		new_password = request.json.get('new_password')

		user_service.change_password(user.email, old_password, new_password)

		return '', 204
