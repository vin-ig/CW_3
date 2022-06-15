PWD_HASH_SALT = b'secret here'
PWD_HASH_ITERATIONS = 100_000

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
