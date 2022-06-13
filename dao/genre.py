from dao.model.genre import Genre
from utils import get_pagination


class GenreDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, uid):
        return self.session.query(Genre).get(uid)

    def get_all(self, page):
        offs, lim = get_pagination(Genre, page)
        return self.session.query(Genre).limit(lim).offset(offs).all()
