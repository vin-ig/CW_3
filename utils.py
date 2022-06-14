import base64
import datetime
import hashlib

from flask import abort, request
import jwt
from constants import SECRET, ALGO, PWD_HASH_SALT, PWD_HASH_ITERATIONS, LIMIT
from dao.model.user import User


def get_hash(password: str):
	"""Хэширует пароль"""
	hash_password = hashlib.pbkdf2_hmac(
		'sha256',
		password.encode('utf-8'),
		PWD_HASH_SALT,
		PWD_HASH_ITERATIONS
	)
	return base64.b64encode(hash_password).decode('utf-8')


def create_data(app, db):
	with app.app_context():
		db.create_all()

		u1 = User(name="vasya", password="vasya", email="vasya@ya.ru", surname="Kozlov")
		u2 = User(name="oleg", password="oleg", email="oleg@ya.ru", surname="Ivanov")
		u3 = User(name="olga", password="olga", email="olga@ya.ru", surname="Petrova")

		users = [u1, u2, u3]
		for user in users:
			user.password = get_hash(user.password)

		with db.session.begin():
			db.session.add_all(users)


def check_keys(data: dict, allowed_keys: set):
	"""Проверяет набор передаваемый ключей"""
	keys = set(data.keys())
	if not keys == allowed_keys:
		raise Exception('Переданы неверные ключи')


def get_pagination(model, page):
	try:
		page = int(page)
		lim = LIMIT
	except (TypeError, ValueError):
		page = 1
		lim = model.query.count()

	offset = (page - 1) * lim
	return offset, lim


def dec(func):
	def wrapper(*args, **kwargs):
		a = 8
		return func(a, *args, **kwargs)
	return wrapper


@dec
def my_func(a):
	return 3 * a

