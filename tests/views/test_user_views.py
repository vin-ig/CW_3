import pytest

from dao.model.user import User


class TestUserView:
    url = "/user/"

    @pytest.fixture
    def user(self, db):
        u = User(email='kk@ya.ru', password='kk')
        db.session.add(u)
        db.session.commit()
        return u

    def test_get_user(self, client, user):
        response = client.get(self.url.format(user_id=user.id))
        assert response.status_code == 401
