from dao.model.director import Director
from utils import get_pagination


class DirectorDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, uid):
        return self.session.query(Director).get(uid)

    def get_all(self, page):
        offs, lim = get_pagination(Director, page)
        return self.session.query(Director).limit(lim).offset(offs).all()
