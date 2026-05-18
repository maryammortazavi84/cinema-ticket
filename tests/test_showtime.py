"""
Test module for ShowTime domain model.
"""

import pytest
from datetime import datetime
from decimal import Decimal

from core.showtime import ShowTime
from utils.exceptions import (
    InvalidMovieIdError,
    InvalidHallNameError,
    InvalidShowtimeError,
)

# ─────────────────────────────────────────────
# 1. CREATE SHOWTIME SUCCESS
# ─────────────────────────────────────────────
def test_create_showtime_success():
    showtime = ShowTime(
        movie_id="m1",
        start_time=datetime(2026, 5, 16, 20, 0),
        hall_name="Hall A",
        price=Decimal("12.50")
    )

    assert showtime.movie_id == "m1"
    assert showtime.hall_name == "Hall A"
    assert showtime.price == Decimal("12.50")
    assert len(showtime.seats) == 50


# ─────────────────────────────────────────────
# 2. INVALID MOVIE ID
# ─────────────────────────────────────────────
def test_invalid_movie_id():
    with pytest.raises(InvalidMovieIdError):
        ShowTime(
            movie_id="",
            start_time=datetime.now(),
            hall_name="Hall A",
            price=Decimal("10")
        )


# ─────────────────────────────────────────────
# 3. INVALID HALL NAME
# ─────────────────────────────────────────────
def test_invalid_hall_name():
    with pytest.raises(InvalidHallNameError):
        ShowTime(
            movie_id="m1",
            start_time=datetime.now(),
            hall_name="   ",
            price=Decimal("10")
        )


# ─────────────────────────────────────────────
# 4. INVALID START TIME TYPE
# ─────────────────────────────────────────────
def test_invalid_start_time():
    with pytest.raises(InvalidShowtimeError):
        ShowTime(
            movie_id="m1",
            start_time="not-a-datetime",
            hall_name="Hall A",
            price=Decimal("10")
        )


# ─────────────────────────────────────────────
# 5. NEGATIVE PRICE
# ─────────────────────────────────────────────
def test_negative_price():
    with pytest.raises(ValueError):
        ShowTime(
            movie_id="m1",
            start_time=datetime.now(),
            hall_name="Hall A",
            price=Decimal("-5")
        )


# ─────────────────────────────────────────────
# 6. TO_DICT SERIALIZATION
# ─────────────────────────────────────────────
def test_to_dict():
    showtime = ShowTime(
        movie_id="m1",
        start_time=datetime(2026, 1, 1, 10, 0),
        hall_name="Hall A",
        price=Decimal("10")
    )

    data = showtime.to_dict()

    assert data["movie_id"] == "m1"
    assert data["hall_name"] == "Hall A"
    assert data["price"] == "10"
    assert "start_time" in data
    assert "seats" in data


# ─────────────────────────────────────────────
# 7. FROM_DICT DESERIALIZATION
# ─────────────────────────────────────────────
def test_from_dict():
    data = {
        "showtime_id": "123",
        "movie_id": "m1",
        "start_time": "2026-01-01T10:00:00",
        "hall_name": "Hall A",
        "price": "10",
        "seats": []
    }

    showtime = ShowTime.from_dict(data)

    assert showtime.movie_id == "m1"
    assert showtime.price == Decimal("10")
    assert showtime.showtime_id == "123"


# ─────────────────────────────────────────────
# 8. SEATS GENERATION
# ─────────────────────────────────────────────
def test_seats_generated():
    showtime = ShowTime(
        movie_id="m1",
        start_time=datetime.now(),
        hall_name="Hall A",
        price=Decimal("10")
    )

    assert len(showtime.seats) == 50