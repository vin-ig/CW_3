from dao.favourites import FavouritesDAO


class FavouritesService:
	def __init__(self, dao: FavouritesDAO):
		self.dao = dao

	def get_one(self, uid):
		return self.dao.get_one(uid)

	def get_all(self):
		return self.dao.get_all()
