import datetime
import jwt
from flask import request
from flask_restx import abort

from constants import SECRET, ALGO


class AuthService:

	@staticmethod
	def auth_required(func):
		"""Проверка аутентификации"""
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

	@staticmethod
	def get_email_from_jwt():
		"""Возвращает email пользователя из токена"""
		user_token = request.headers.get('Authorization').split()[-1]
		decode_data = jwt.decode(user_token, SECRET, ALGO)
		return decode_data.get('email')

	@staticmethod
	def generate_jwt(user_obj: dict) -> dict:
		"""Генерирует пару access_token/refresh_token"""
		min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
		days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
		user_obj['exp'] = min30
		access_token = jwt.encode(user_obj, SECRET, algorithm=ALGO)
		user_obj['exp'] = datetime.datetime.timestamp(days130)
		refresh_token = jwt.encode(user_obj, SECRET, algorithm=ALGO)
		return {"access_token": access_token, "refresh_token": refresh_token}
