from flask import Flask, render_template
from flask_restx import Api

from config import Config
from setup_db import db

from views.auth import auth_ns
from views.directors import director_ns
from views.favourites import favourites_ns
from views.genres import genre_ns
from views.movies import movie_ns
from views.user import user_ns


def register_extensions(app):
    db.init_app(app)
    api = Api(app, title="Flask Course Project 4", doc="/docs")
    api.add_namespace(director_ns)
    api.add_namespace(genre_ns)
    api.add_namespace(movie_ns)
    api.add_namespace(auth_ns)
    api.add_namespace(user_ns)
    api.add_namespace(favourites_ns)


app = Flask(__name__)
app.config.from_object(Config())


@app.route('/')
def index():
    return render_template('index.html')


register_extensions(app)

if __name__ == '__main__':
    app.run(port=25000)
