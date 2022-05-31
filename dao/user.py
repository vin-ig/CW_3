from dao.model.user import User


class UserDAO:
	def __init__(self, session):
		self.session = session

	def get_one_by_id(self, uid):
		return self.session.query(User).get(uid)

	def get_one(self, name):
		return self.session.query(User).filter(User.username == name).first()

	def get_all(self):
		return self.session.query(User).all()

	def create(self, user_d):
		ent = User(**user_d)
		self.session.add(ent)
		self.session.commit()
		return ent

	def delete(self, uid):
		user = self.get_one(uid)
		self.session.delete(user)
		self.session.commit()

	def update(self, user_d):
		user = self.get_one(user_d.get("id"))
		user.name = user_d.get("name")

		self.session.add(user)
		self.session.commit()
