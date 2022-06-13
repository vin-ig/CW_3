import datetime

import jwt
from flask import request, abort
from flask_restx import Namespace, Resource

from constants import SECRET, ALGO, TOKEN_KEYS, USER_KEYS
from dao.model.movie import MovieSchema
from dao.model.user import UserSchema
from implemented import user_service, auth_service, movie_service, favourites_service
from utils import check_keys


favourites_ns = Namespace('favorites')

movie_s = MovieSchema()
movies_s = MovieSchema(many=True)


@favourites_ns.route('/movies/')
class FavouritesView(Resource):
	def get(self):
		"""Выводит избранные фильмы"""
		page = request.args.get('page')
		movies = favourites_service.get_all(page, status=None)

		return movies_s.dump(movies), 200


# @favourites_ns.route('/login/')
# class AuthLoginVIew(Resource):
# 	def post(self):
# 		"""Авторизация пользователя"""
# 		email = request.json.get('email')
# 		password = request.json.get('password')
#
# 		try:
# 			user = user_service.get_one(email)
# 			user_service.check_password(user.email, password)
# 			# user_service.__compare_password(user.password, password)
# 		except Exception:
# 			abort(401)
#
# 		user_dict = UserSchema().dump(user)
# 		return auth_service.generate_jwt(user_dict), 201
#
# 	def put(self):
# 		"""Генерация новых токенов"""
# 		# access_token = request.json.get('access_token')
# 		token = request.json.get('refresh_token')
#
# 		try:
# 			decode_token = jwt.decode(token, SECRET, ALGO)
# 			time = datetime.datetime.fromtimestamp(decode_token['exp'])
# 			check_keys(decode_token, TOKEN_KEYS)
# 			if datetime.datetime.utcnow() > time:
# 				raise Exception('Expired token')
# 			return auth_service.generate_jwt(decode_token), 201
# 		except Exception as error:
# 			return f'{error}', 200
