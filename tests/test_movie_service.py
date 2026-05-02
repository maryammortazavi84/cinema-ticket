import pytest
from core.movie import Movie
from core.enums import AgeRating
from utils.exceptions import MovieNotFoundError

import services.movie_service as ms


# -----------------------
# Helpers
# -----------------------

def fake_movies():
    return [
        {
            "movie_id": "1",
            "title": "Batman",
            "duration_minutes": 120,
            "age_rating": AgeRating.PG13.value,
            "genre": "Action"
        },
        {
            "movie_id": "2",
            "title": "Joker",
            "duration_minutes": 122,
            "age_rating": AgeRating.R.value,
            "genre": "Drama"
        }
    ]


# -----------------------
# ADD MOVIE
# -----------------------

def test_add_movie_success(monkeypatch):
    monkeypatch.setattr(ms, "load_movies", lambda: [])
    monkeypatch.setattr(ms, "save_movies", lambda x: None)

    movie = ms.add_movie(
        title="Inception",
        duration_minutes=148,
        age_rating=AgeRating.PG13,
        genre="Sci-Fi"
    )

    assert isinstance(movie, Movie)
    assert movie.title == "Inception"


# -----------------------
# GET ALL MOVIES
# -----------------------

def test_get_all_movies(monkeypatch):
    monkeypatch.setattr(ms, "load_movies", lambda: fake_movies())

    movies = ms.get_all_movies()

    assert len(movies) == 2
    assert all(isinstance(m, Movie) for m in movies)
    assert movies[0].title == "Batman"


# -----------------------
# GET BY ID - SUCCESS
# -----------------------

def test_get_movie_by_id_success(monkeypatch):
    monkeypatch.setattr(ms, "load_movies", lambda: fake_movies())

    movie = ms.get_movie_by_id("1")

    assert movie.movie_id == "1"
    assert movie.title == "Batman"


# -----------------------
# GET BY ID - NOT FOUND
# -----------------------

def test_get_movie_by_id_not_found(monkeypatch):
    monkeypatch.setattr(ms, "load_movies", lambda: fake_movies())

    with pytest.raises(MovieNotFoundError):
        ms.get_movie_by_id("999")


# -----------------------
# SEARCH MOVIES
# -----------------------

def test_search_movies_by_title(monkeypatch):
    monkeypatch.setattr(ms, "load_movies", lambda: fake_movies())

    results = ms.search_movies_by_title("bat")

    assert len(results) == 1
    assert results[0].title == "Batman"

    results2 = ms.search_movies_by_title("joker")

    assert len(results2) == 1
    assert results2[0].title == "Joker"