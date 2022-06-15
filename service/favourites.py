from dao.favourites import FavouritesDAO


class FavouritesService:
	def __init__(self, dao: FavouritesDAO):
		self.dao = dao

	def get_one(self, uid):
		return self.dao.get_one(uid)

	def get_all(self, uid):
		return self.dao.get_all(uid)

	def add(self, user_id, movie_id):
		data = {}
		data['user_id'] = user_id
		data['movie_id'] = movie_id
		return self.dao.add(data)
