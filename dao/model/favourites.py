from setup_db import db
from marshmallow import Schema, fields


class Favourites(db.Model):
	__tablename__ = "favourites"
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
	movie_id = db.Column(db.Integer, db.ForeignKey("movie.id"), nullable=False)
	user = db.relationship("User")
	movie = db.relationship("Movie")


class FavouritesSchema(Schema):
	id = fields.Int()
	user_id = fields.Int()
	movie_id = fields.Int()
