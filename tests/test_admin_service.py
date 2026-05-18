import pytest
from unittest.mock import patch

from core.movie import Movie
from core.showtime import ShowTime
from core.enums import AgeRating
from services.admin_service import add_movie, delete_movie, add_showtime, delete_showtime
from utils.exceptions import CinemaTicketError
from decimal import Decimal
from datetime import datetime


# -----------------------------
# ADD MOVIE
# -----------------------------
@patch("services.admin_service.load_movies")
@patch("services.admin_service.save_movies")
def test_add_movie_increases_storage(mock_save, mock_load):
    mock_load.return_value = []

    movie = Movie(
        title="Test Movie",
        duration_minutes=120,
        age_rating=AgeRating.PG,
        genre="Action"
    )

    add_movie(movie)

    saved = mock_save.call_args[0][0]

    assert len(saved) == 1
    assert saved[0]["title"] == "Test Movie"


# -----------------------------
# DELETE MOVIE SUCCESS
# -----------------------------
@patch("services.admin_service.load_movies")
@patch("services.admin_service.save_movies")
def test_delete_movie_removes_it(mock_save, mock_load):
    mock_load.return_value = [
        {"movie_id": "1", "title": "A"},
        {"movie_id": "2", "title": "B"},
    ]

    delete_movie("1")

    saved = mock_save.call_args[0][0]
    assert len(saved) == 1
    assert saved[0]["movie_id"] == "2"


# -----------------------------
# DELETE MOVIE NOT FOUND
# -----------------------------
@patch("services.admin_service.load_movies")
@patch("services.admin_service.save_movies")
def test_delete_movie_not_found_raises(mock_save, mock_load):
    mock_load.return_value = [{"movie_id": "1"}]

    with pytest.raises(CinemaTicketError):
        delete_movie("999")


# -----------------------------
# ADD SHOWTIME SUCCESS
# -----------------------------
@patch("services.admin_service.load_movies")
@patch("services.admin_service.load_showtimes")
@patch("services.admin_service.save_showtimes")
def test_add_showtime_success(mock_save, mock_load_showtimes, mock_load_movies):
    mock_load_movies.return_value = [{"movie_id": "1"}]
    mock_load_showtimes.return_value = []

    showtime = ShowTime(
        movie_id="1",
        start_time=datetime(2030, 1, 1, 20, 0),
        hall_name="Hall A",
        price=Decimal("10.00")
    )

    add_showtime(showtime)

    saved = mock_save.call_args[0][0]
    assert len(saved) == 1
    assert saved[0]["movie_id"] == "1"


# -----------------------------
# ADD SHOWTIME WITHOUT MOVIE
# -----------------------------
@patch("services.admin_service.load_movies")
@patch("services.admin_service.load_showtimes")
def test_add_showtime_without_movie_raises(mock_load_showtimes, mock_load_movies):
    mock_load_movies.return_value = []
    mock_load_showtimes.return_value = []

    showtime = ShowTime(
        movie_id="404",
        start_time=datetime(2030, 1, 1, 20, 0),
        hall_name="Hall A",
        price=Decimal("10.00")
    )

    with pytest.raises(CinemaTicketError):
        add_showtime(showtime)


# -----------------------------
# DELETE SHOWTIME SUCCESS
# -----------------------------
@patch("services.admin_service.load_showtimes")
@patch("services.admin_service.save_showtimes")
def test_delete_showtime_success(mock_save, mock_load):
    mock_load.return_value = [
        {"showtime_id": "1"},
        {"showtime_id": "2"},
    ]

    delete_showtime("1")

    saved = mock_save.call_args[0][0]
    assert len(saved) == 1
    assert saved[0]["showtime_id"] == "2"


# -----------------------------
# DELETE SHOWTIME NOT FOUND
# -----------------------------
@patch("services.admin_service.load_showtimes")
@patch("services.admin_service.save_showtimes")
def test_delete_showtime_not_found_raises(mock_save, mock_load):
    mock_load.return_value = [{"showtime_id": "1"}]

    with pytest.raises(CinemaTicketError):
        delete_showtime("999")