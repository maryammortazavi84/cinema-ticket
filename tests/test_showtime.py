import pytest
from datetime import datetime

from core.showtime import ShowTime
from core.seat import Seat
from utils.exceptions import (
    InvalidShowtimeError,
    InvalidHallNameError,
    InvalidMovieIdError,
    InvalidSeatError,
)


def test_create_showtime_success():
    showtime = ShowTime(
        movie_id="movie123",
        start_time=datetime(2026, 5, 14, 20, 0),
        hall_name="Hall 1"
    )

    assert showtime.movie_id == "movie123"
    assert showtime.hall_name == "Hall 1"
    assert isinstance(showtime.start_time, datetime)
    assert len(showtime.seats) == 50


def test_invalid_movie_id():
    with pytest.raises(InvalidMovieIdError):
        ShowTime(
            movie_id="",
            start_time=datetime.now(),
            hall_name="Hall 1"
        )


def test_invalid_start_time():
    with pytest.raises(InvalidShowtimeError):
        ShowTime(
            movie_id="movie123",
            start_time="20:00",
            hall_name="Hall 1"
        )


def test_invalid_hall_name():
    with pytest.raises(InvalidHallNameError):
        ShowTime(
            movie_id="movie123",
            start_time=datetime.now(),
            hall_name=""
        )


def test_generate_seats():
    showtime = ShowTime(
        movie_id="movie123",
        start_time=datetime.now(),
        hall_name="Hall 1"
    )

    assert len(showtime.seats) == 50
    assert isinstance(showtime.seats[0], Seat)


def test_get_seat_success():
    showtime = ShowTime(
        movie_id="movie123",
        start_time=datetime.now(),
        hall_name="Hall 1"
    )

    seat = showtime.get_seat("A", 1)

    assert seat.row == "A"
    assert seat.number == 1


def test_get_seat_not_found():
    showtime = ShowTime(
        movie_id="movie123",
        start_time=datetime.now(),
        hall_name="Hall 1"
    )

    with pytest.raises(InvalidSeatError):
        showtime.get_seat("Z", 99)


def test_get_available_seats():
    showtime = ShowTime(
        movie_id="movie123",
        start_time=datetime.now(),
        hall_name="Hall 1"
    )

    seat = showtime.get_seat("A", 1)
    seat.reserve()

    available_seats = showtime.get_available_seats()

    assert len(available_seats) == 49
    assert seat not in available_seats


def test_showtime_to_dict():
    showtime = ShowTime(
        movie_id="movie123",
        start_time=datetime(2026, 5, 14, 20, 0),
        hall_name="Hall 1"
    )

    data = showtime.to_dict()

    assert data["movie_id"] == "movie123"
    assert data["hall_name"] == "Hall 1"
    assert isinstance(data["seats"], list)
    assert len(data["seats"]) == 50


def test_showtime_from_dict():
    data = {
        "showtime_id": "show123",
        "movie_id": "movie123",
        "start_time": "2026-05-14T20:00:00",
        "hall_name": "Hall 1",
        "seats": [
            {
                "row": "A",
                "number": 1,
                "is_available": False
            }
        ]
    }

    showtime = ShowTime.from_dict(data)

    assert showtime.showtime_id == "show123"
    assert showtime.movie_id == "movie123"

    seat = showtime.get_seat("A", 1)

    assert seat.is_available is False


def test_showtime_str():
    showtime = ShowTime(
        movie_id="movie123",
        start_time=datetime.now(),
        hall_name="Hall 1"
    )

    result = str(showtime)

    assert "Showtime ID:" in result
    assert "Movie ID:" in result
    assert "Available Seats:" in result