import pytest

from dao.model.movie import Movie


class TestMoviesView:
    url = "/movies/"

    @pytest.fixture
    def movie(self, db):
        m = Movie(title="ff", description="ff", trailer="ff", year=13, rating=13, genre_id=13, director_id=13)
        db.session.add(m)
        db.session.commit()
        return m

    def test_get_movies(self, client, movie):
        response = client.get(self.url)
        assert response.status_code == 200
        assert response.json == [{"id": movie.id,
                                 "title": movie.title,
                                 "description": movie.description,
                                 "trailer": movie.trailer,
                                 "year": movie.year,
                                 "rating": movie.rating,
                                 "genre": None,
                                 "director": None
                                 }]


class TestMovieView:
    url = "/movies/{movie_id}/"

    @pytest.fixture
    def movie(self, db):
        m = Movie(title="ff", description="ff", trailer="ff", year=13, rating=13, genre_id=13, director_id=13)
        db.session.add(m)
        db.session.commit()
        return m

    def test_get_movie(self, client, movie):
        response = client.get(self.url.format(movie_id=movie.id))
        assert response.status_code == 200
        assert response.json == {"id": movie.id,
                                 "title": movie.title,
                                 "description": movie.description,
                                 "trailer": movie.trailer,
                                 "year": movie.year,
                                 "rating": movie.rating,
                                 "genre": None,
                                 "director": None
                                 }

    def test_movie_not_found(self, client):
        response = client.get(self.url.format(movie_id=None))
        assert response.status_code == 404
