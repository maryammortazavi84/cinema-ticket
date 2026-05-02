import pytest

from core.movie import Movie
from core.enums import AgeRating
from utils.exceptions import (
    InvalidMovieTitleError,
    InvalidDurationError,
    InvalidAgeRatingError,
    InvalidGenreError,
)


# -------------------------
# Success case
# -------------------------

def test_create_movie_success():
    movie = Movie(
        title="Interstellar",
        duration_minutes=169,
        age_rating=AgeRating.PG13,
        genre="Sci-Fi"
    )

    assert movie.title == "Interstellar"
    assert movie.duration_minutes == 169
    assert movie.age_rating == AgeRating.PG13
    assert movie.genre == "Sci-Fi"
    assert movie.movie_id is not None


# -------------------------
# Title validation
# -------------------------

def test_movie_invalid_title_empty():
    with pytest.raises(InvalidMovieTitleError):
        Movie(
            title="",
            duration_minutes=120,
            age_rating=AgeRating.PG13,
            genre="Action"
        )


# -------------------------
# Duration validation
# -------------------------

def test_movie_invalid_duration():
    with pytest.raises(InvalidDurationError):
        Movie(
            title="Batman",
            duration_minutes=0,
            age_rating=AgeRating.PG13,
            genre="Action"
        )


# -------------------------
# Age rating validation
# -------------------------

def test_movie_invalid_age_rating():
    with pytest.raises(InvalidAgeRatingError):
        Movie(
            title="Batman",
            duration_minutes=120,
            age_rating="PG13",  # invalid
            genre="Action"
        )


# -------------------------
# Genre validation
# -------------------------

def test_movie_invalid_genre():
    with pytest.raises(InvalidGenreError):
        Movie(
            title="Batman",
            duration_minutes=120,
            age_rating=AgeRating.PG13,
            genre=""
        )


# -------------------------
# Serialization
# -------------------------

def test_movie_to_dict():
    movie = Movie(
        title="Inception",
        duration_minutes=148,
        age_rating=AgeRating.PG13,
        genre="Sci-Fi"
    )

    data = movie.to_dict()

    assert data["title"] == "Inception"
    assert data["duration_minutes"] == 148
    assert data["age_rating"] == AgeRating.PG13.value
    assert data["genre"] == "Sci-Fi"


# -------------------------
# Deserialization
# -------------------------

def test_movie_from_dict():
    data = {
        "movie_id": "abc123",
        "title": "Joker",
        "duration_minutes": 122,
        "age_rating": AgeRating.R.value,
        "genre": "Drama"
    }

    movie = Movie.from_dict(data)

    assert movie.movie_id == "abc123"
    assert movie.title == "Joker"
    assert movie.duration_minutes == 122
    assert movie.age_rating == AgeRating.R
    assert movie.genre == "Drama"