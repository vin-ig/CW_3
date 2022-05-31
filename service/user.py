import hashlib
from constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS


class UserService:
	def __init__(self, dao):
		self.dao = dao

	def get_one(self, name):
		return self.dao.get_one(name)

	def get_hash(self, password):
		return hashlib.pbkdf2_hmac(
					'sha256',
					password.encode('utf-8'),
					PWD_HASH_SALT,
					PWD_HASH_ITERATIONS
				).decode("utf-8", "ignore")

	def check_password(self, name, other_password):
		user = self.dao.get_one(name)
		pwd_hash = self.get_hash(other_password)
		if pwd_hash != user.password:
			raise Exception('Invalid password')

	def create(self, new_user):
		new_user['password'] = self.get_hash(new_user['password'])
		return self.dao.create(new_user)
