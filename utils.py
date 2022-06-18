import base64
import hashlib

from constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS, LIMIT
from dao.model.user import User
from flask_restx import fields as flask_fields
from marshmallow import fields as marshmallow_fields


def convert_schema_to_flask_model(schema):
	"""Конвертирует поля моделей из marshmallow в flask"""
	TYPE_MAPPING = {
		marshmallow_fields.String: flask_fields.String,
		marshmallow_fields.Integer: flask_fields.Integer,
		marshmallow_fields.DateTime: flask_fields.DateTime,
		marshmallow_fields.Float: flask_fields.Float,
		marshmallow_fields.Nested: flask_fields.Nested,
	}
	schema_fields = getattr(schema, "_declared_fields")
	converted_schema = {}

	for field in schema_fields:
		converted_schema[field] = TYPE_MAPPING[type(schema_fields[field])]

	return converted_schema


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
	"""Наполнение таблицы данными"""
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
	"""Определяет параметры для пагинации"""
	try:
		page = int(page)
		lim = LIMIT
	except (TypeError, ValueError):
		page = 1
		lim = model.query.count()

	offset = (page - 1) * lim
	return offset, lim
