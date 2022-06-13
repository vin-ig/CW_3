import base64
import hashlib
import hmac

from constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS


class UserService:
	def __init__(self, dao):
		self.dao = dao

	def get_one(self, email):
		return self.dao.get_one(email)

	def get_one_by_id(self, uid):
		return self.dao.get_one_by_id(uid)

	@staticmethod
	def get_hash(password: str) -> str:
		hash_p = hashlib.pbkdf2_hmac(
					'sha256',
					password.encode('utf-8'),
					PWD_HASH_SALT,
					PWD_HASH_ITERATIONS
				)
		return base64.b64encode(hash_p).decode('utf-8')

	def check_password(self, email, other_password):
		user = self.dao.get_one(email)
		pwd_hash = self.get_hash(other_password)
		if pwd_hash != user.password:
			raise Exception('Invalid password')

	@staticmethod
	def __compare_password(password_1, password_2):
		return hmac.compare_digest(password_1, password_2)

	def create(self, new_user):
		new_user['password'] = self.get_hash(new_user['password'])
		return self.dao.create(new_user)

	def update(self, data: dict, email: str):
		user = self.dao.get_one(email)

		user.email = data.get('email', user.email)
		user.name = data.get('name', user.name)
		user.surname = data.get('surname', user.surname)
		user.favourite_genre = data.get('favourite_genre', user.favourite_genre)

		self.dao.update(user)

	def change_password(self, email, old_password, new_password):
		user = self.dao.get_one(email)
		pwd_hash = self.get_hash(old_password)
		if pwd_hash != user.password:
			raise Exception('Invalid password')
		user.password = self.get_hash(new_password)
		return self.dao.update(user)
