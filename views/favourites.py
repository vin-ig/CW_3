from flask_restx import Namespace, Resource

from dao.model.movie import MovieSchema
from implemented import user_service, auth_service, favourites_service


favourites_ns = Namespace('favorites')
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
		return '', 201

	@auth_service.auth_required
	def delete(self, uid):
		favourites_service.delete(uid)
		return '', 204
