import base64
import datetime
import hashlib

import jwt
from flask import request
from flask_restx import abort

from constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS, SECRET, ALGO


class AuthService:
	@staticmethod
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

	@staticmethod
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
