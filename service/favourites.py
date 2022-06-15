from dao.favourites import FavouritesDAO


class FavouritesService:
	def __init__(self, dao: FavouritesDAO):
		self.dao = dao

	def get_all(self, uid):
		return self.dao.get_all(uid)

	def add(self, user_id, movie_id):
		data = {'user_id': user_id, 'movie_id': movie_id}
		return self.dao.add(data)

	def delete(self, movie_id):
		self.dao.delete(movie_id)
