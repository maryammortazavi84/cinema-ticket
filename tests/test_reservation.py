import pytest
from decimal import Decimal
from datetime import datetime, timedelta

from services.reservation_service import (
    reserve_ticket,
    _check_valid_showtime,
)

from core.showtime import ShowTime
from utils.exceptions import (
    InvalidUserIdError,
    InvalidShowtimeError,
    SeatAlreadyReservedError,
)

from storage.json_storage import (
    save_showtimes,
    save_tickets,
    load_showtimes,
    load_tickets,
)


@pytest.fixture
def clean_storage():
    """Clean JSON storage before each test."""
    save_showtimes([])
    save_tickets([])


def create_future_showtime():
    """Helper function to create and save a valid future showtime."""
    showtime = ShowTime(
        movie_id="movie_123",
        start_time=datetime.now() + timedelta(hours=2),
        hall_name="Hall 1"
    )

    showtimes = load_showtimes()
    showtimes.append(showtime.to_dict())
    save_showtimes(showtimes)

    return showtime


def test_check_valid_showtime_returns_showtime(clean_storage):
    showtime = create_future_showtime()

    result = _check_valid_showtime(showtime.showtime_id)

    assert result.showtime_id == showtime.showtime_id


def test_check_valid_showtime_raises_error_for_invalid_id(clean_storage):
    with pytest.raises(InvalidShowtimeError):
        _check_valid_showtime("invalid_id")


def test_reserve_ticket_success(clean_storage):
    showtime = create_future_showtime()

    ticket = reserve_ticket(
        user_id="user_123",
        showtime_id=showtime.showtime_id,
        seat_row="A",
        seat_number=1,
        price=Decimal("15.99")
    )

    assert ticket.user_id == "user_123"
    assert ticket.showtime_id == showtime.showtime_id
    assert ticket.seat_row == "A"
    assert ticket.seat_number == 1


def test_reserved_seat_becomes_unavailable(clean_storage):
    showtime = create_future_showtime()

    reserve_ticket(
        user_id="user_123",
        showtime_id=showtime.showtime_id,
        seat_row="A",
        seat_number=1,
        price=Decimal("15.99")
    )

    updated_showtime_data = load_showtimes()[0]
    updated_showtime = ShowTime.from_dict(updated_showtime_data)

    seat = updated_showtime.get_seat("A", 1)

    assert seat.is_available is False


def test_cannot_reserve_already_reserved_seat(clean_storage):
    showtime = create_future_showtime()

    reserve_ticket(
        user_id="user_123",
        showtime_id=showtime.showtime_id,
        seat_row="A",
        seat_number=1,
        price=Decimal("15.99")
    )

    with pytest.raises(SeatAlreadyReservedError):
        reserve_ticket(
            user_id="user_456",
            showtime_id=showtime.showtime_id,
            seat_row="A",
            seat_number=1,
            price=Decimal("15.99")
        )


def test_reserve_ticket_with_invalid_user_id(clean_storage):
    showtime = create_future_showtime()

    with pytest.raises(InvalidUserIdError):
        reserve_ticket(
            user_id="",
            showtime_id=showtime.showtime_id,
            seat_row="A",
            seat_number=1,
            price=Decimal("15.99")
        )


def test_ticket_is_saved_after_reservation(clean_storage):
    showtime = create_future_showtime()

    reserve_ticket(
        user_id="user_123",
        showtime_id=showtime.showtime_id,
        seat_row="B",
        seat_number=5,
        price=Decimal("20.00")
    )

    tickets = load_tickets()

    assert len(tickets) == 1
    assert tickets[0]["seat_row"] == "B"
    assert tickets[0]["seat_number"] == 5