from setup_db import db
from marshmallow import Schema, fields


class User(db.Model):
	__tablename__ = 'user'
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(50), unique=True, nullable=False)
	password = db.Column(db.String, nullable=False)
	name = db.Column(db.String(50))
	surname = db.Column(db.String(50))
	favourite_genre = db.Column(db.Integer, db.ForeignKey('genre.id'))
	genre = db.relationship("Genre")


class UserSchema(Schema):
	id = fields.Int()
	email = fields.Str()
	password = fields.Str()
	name = fields.Str()
	surname = fields.Str()
	favourite_genre = fields.Int()
