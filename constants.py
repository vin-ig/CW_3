from dao.model.director import Director
from dao.model.movie import Movie

PWD_HASH_SALT = b'secret here'
PWD_HASH_ITERATIONS = 100_000

QUERY = (
	Movie.id,
	Movie.title,
	Movie.description,
	Movie.trailer,
	Movie.year,
	Movie.rating,
	# Director.name.label('director'),
	# Genre.name.label('genre')
)

# Допустимые ключи для проверки
USER_KEYS = {'email', 'password'}
TOKEN_KEYS = {'email', 'exp', 'id', 'password', 'name', 'surname', 'favourite_genre'}
MOVIE_KEYS = {'title', 'description', 'trailer', 'year', 'rating', 'genre_id', 'director_id'}
DIRECTOR_KEYS = {'name'}
GENRE_KEYS = {'name'}

SECRET = 's3cR$eT'
ALGO = 'HS256'

# Количество объектов на странице
LIMIT = 12
