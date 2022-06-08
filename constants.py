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
USER_KEYS = {'username', 'role', 'password'}
TOKEN_KEYS = {'username', 'role', 'exp', 'id', 'password'}
MOVIE_KEYS = {'title', 'description', 'trailer', 'year', 'rating', 'genre_id', 'director_id'}
DIRECTOR_KEYS = {'name'}
GENRE_KEYS = {'name'}

SECRET = 's3cR$eT'
ALGO = 'HS256'

LIMIT = 4
