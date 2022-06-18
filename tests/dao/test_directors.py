import pytest

from dao.director import DirectorDAO
from dao.model.director import Director


class TestDirectorDAO:
	@pytest.fixture(autouse=True)
	def dao(self, db):
		self.dao = DirectorDAO(db.session)

	@pytest.fixture
	def director_1(self, db):
		d = Director(name="Стивен Спилберг")
		db.session.add(d)
		db.session.commit()
		return d

	@pytest.fixture
	def director_2(self, db):
		d = Director(name="Вуди Аллен")
		db.session.add(d)
		db.session.commit()
		return d

	def test_get_director_by_id(self, director_1):
		assert self.dao.get_one(director_1.id) == director_1

	def test_get_director_by_id_not_found(self):
		assert self.dao.get_one(1) is None

	def test_get_all_directors(self, director_1, director_2):
		assert self.dao.get_all(1) == [director_1, director_2]
