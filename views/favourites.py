from flask_restx import Namespace, Resource

from dao.model.movie import MovieSchema
from implemented import user_service, auth_service, favourites_service

favourites_ns = Namespace('favorites')
movies_s = MovieSchema(many=True)


@favourites_ns.route('/movies/')
class FavouritesView(Resource):
	@favourites_ns.response(200, description='Success')
	@favourites_ns.doc(description='Список избранных фильмов')
	@auth_service.auth_required
	def get(self):
		"""Выводит избранные фильмы"""
		email = auth_service.get_email_from_jwt()
		user = user_service.get_one(email)
		movies = favourites_service.get_all(user.id)
		return movies_s.dump(movies), 200


@favourites_ns.route('/movies/<int:uid>/')
class FavouriteView(Resource):
	@favourites_ns.response(201, description='Фильм добавлен')
	@favourites_ns.doc(params={'uid': 'Movie ID'}, description='Добавление фильма в избранное')
	@auth_service.auth_required
	def post(self, uid):
		"""Добавляет фильм в избранное"""
		email = auth_service.get_email_from_jwt()
		user = user_service.get_one(email)
		favourites_service.add(user_id=user.id, movie_id=uid)
		return '', 201

	@favourites_ns.response(204, description='Фильм удален')
	@favourites_ns.doc(params={'uid': 'Movie ID'}, description='Удаление фильма из избранного')
	@auth_service.auth_required
	def delete(self, uid):
		"""Удаляет фильм из избранного"""
		favourites_service.delete(uid)
		return '', 204
