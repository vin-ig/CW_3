from setup_db import db
from marshmallow import Schema, fields


class UserMovie(db.Model):
	__tablename__ = "user_movie"
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
	movie_id = db.Column(db.Integer, db.ForeignKey("movie.id"), nullable=False)
	user = db.relationship("User")
	movie = db.relationship("Movie")


class UserMovieSchema(Schema):
	id = fields.Int()
	user_id = fields.Int()
	movie_id = fields.Int()
