import datetime

import jwt
from flask import request, abort
from flask_restx import Namespace, Resource

from constants import SECRET, ALGO, TOKEN_KEYS, USER_KEYS
from dao.model.favourites import FavouritesSchema
from dao.model.movie import MovieSchema
from dao.model.user import UserSchema
from implemented import user_service, auth_service, movie_service, favourites_service
from utils import check_keys


favourites_ns = Namespace('favorites')

favourite_s = FavouritesSchema()
favourites_s = FavouritesSchema(many=True)
movies_s = MovieSchema(many=True)


@favourites_ns.route('/movies/')
class FavouritesView(Resource):
	@auth_service.auth_required
	def get(self):
		"""Выводит избранные фильмы"""
		email = auth_service.get_email_from_jwt()
		user = user_service.get_one(email)
		movies = favourites_service.get_all(user.id)
		return movies_s.dump(movies), 200


@favourites_ns.route('/movies/<int:uid>/')
class FavouriteView(Resource):
	@auth_service.auth_required
	def post(self, uid):
		email = auth_service.get_email_from_jwt()
		user = user_service.get_one(email)
		favourites_service.add(user_id=user.id, movie_id=uid)
		return '', 200