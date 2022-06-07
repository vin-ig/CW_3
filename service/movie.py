from dao.movie import MovieDAO


class MovieService:
	def __init__(self, dao: MovieDAO):
		self.dao = dao

	def get_one(self, uid):
		return self.dao.get_one_join(uid)

	def get_all(self, page, status):
		return self.dao.get_all(page, status)

	def create(self, data):
		return self.dao.create(data)

	def update(self, data, uid):
		movie = self.dao.get_one(uid)

		movie.title = data.get('title', movie.title)
		movie.description = data.get('description', movie.description)
		movie.trailer = data.get('trailer', movie.trailer)
		movie.year = data.get('year', movie.year)
		movie.rating = data.get('rating', movie.rating)
		movie.genre_id = data.get('genre_id', movie.genre_id)
		movie.director_id = data.get('director_id', movie.director_id)

		self.dao.update(movie)

	def delete(self, uid):
		self.dao.delete(uid)
