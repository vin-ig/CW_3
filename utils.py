import datetime
import hashlib

from flask import abort, request
import jwt
from constants import SECRET, ALGO, PWD_HASH_SALT, PWD_HASH_ITERATIONS
from dao.model.user import User


def get_hash(password: str):
	"""Хэширует пароль"""
	return hashlib.pbkdf2_hmac(
		'sha256',
		password.encode('utf-8'),
		PWD_HASH_SALT,
		PWD_HASH_ITERATIONS
	).decode("utf-8", "ignore")


def create_data(app, db):
	with app.app_context():
		db.create_all()

		u1 = User(username="vasya", password="my_little_pony", role="user")
		u2 = User(username="oleg", password="qwerty", role="user")
		u3 = User(username="olga", password="P@ssw0rd", role="admin")

		users = [u1, u2, u3]
		for user in users:
			user.password = get_hash(user.password)

		with db.session.begin():
			db.session.add_all(users)


def generate_jwt(user_obj: dict) -> dict:
	"""Генерирует пару access_token/refresh_token"""
	min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
	days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
	user_obj['exp'] = min30
	access_token = jwt.encode(user_obj, SECRET, algorithm=ALGO)
	# user_obj['exp'] = days130
	user_obj['exp'] = datetime.datetime.timestamp(days130)
	refresh_token = jwt.encode(user_obj, SECRET, algorithm=ALGO)
	return {"access_token": access_token, "refresh_token": refresh_token}


def check_keys(data: dict, allowed_keys: set):
	"""Проверяет набор передаваемый ключей"""
	keys = set(data.keys())
	if not keys == allowed_keys:
		raise Exception('Переданы неверные ключи')


def auth_required(func):
	def wrapper(*args, **kwargs):
		if 'Authorization' not in request.headers:
			abort(401)
		try:
			user_token = request.headers.get('Authorization').split()[-1]
			jwt.decode(user_token, SECRET, ALGO)
			return func(*args, **kwargs)
		except:
			return abort(401)
	return wrapper


def admin_required(func):
	def wrapper(*args, **kwargs):
		if 'Authorization' not in request.headers:
			abort(401)
		try:
			token = request.headers.get('Authorization').split()[-1]
			user = jwt.decode(token, SECRET, ALGO)
			role = user.get('role')
		except Exception:
			abort(401)
		if role != 'admin':
			abort(403)
		return func(*args, **kwargs)
	return wrapper
