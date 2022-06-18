import pytest

from dao.user import UserDAO
from dao.model.user import User


class TestUserDAO:
	@pytest.fixture(autouse=True)
	def dao(self, db):
		self.dao = UserDAO(db.session)

	@pytest.fixture
	def user_1(self, db):
		u = User(email='kk@ya.ru', password='kk')
		db.session.add(u)
		db.session.commit()
		return u

	def test_get_user_by_email(self, user_1):
		print(user_1.email)
		assert self.dao.get_one(user_1.email) == user_1

	def test_get_user_by_email_not_found(self):
		assert self.dao.get_one("email") is None

	def test_create_users(self):
		u = {'email': 'bek@ya.ru', 'password': 'bek'}
		assert self.dao.create(u).id is not None
