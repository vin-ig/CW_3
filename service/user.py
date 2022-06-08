import hashlib
from constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS


class UserService:
	def __init__(self, dao):
		self.dao = dao

	def get_one(self, email):
		return self.dao.get_one(email)

	def get_hash(self, password):
		return hashlib.pbkdf2_hmac(
					'sha256',
					password.encode('utf-8'),
					PWD_HASH_SALT,
					PWD_HASH_ITERATIONS
				).decode("utf-8", "ignore")

	def check_password(self, email, other_password):
		user = self.dao.get_one(email)
		pwd_hash = self.get_hash(other_password)
		if pwd_hash != user.password:
			raise Exception('Invalid password')

	def create(self, new_user):
		new_user['password'] = self.get_hash(new_user['password'])
		return self.dao.create(new_user)

	def update(self, data, uid):
		user = self.dao.get_one(uid)

		user.email = data.get('email', user.email)
		user.password = data.get('password', user.password)
		user.name = data.get('name', user.name)
		user.surname = data.get('surname', user.surname)
		user.favourite_genre = data.get('favourite_genre', user.favourite_genre)
		
		self.dao.update(user)
