from dao.movie import MovieDAO


class MovieService:
	def __init__(self, dao: MovieDAO):
		self.dao = dao

	def get_one(self, uid):
		return self.dao.get_one(uid)

	def get_all(self, page, status):
		return self.dao.get_all(page, status)

	def get_favourites(self, user_id):
		return self.dao.get_favourites(user_id)

