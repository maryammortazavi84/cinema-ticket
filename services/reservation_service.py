"""
Module: reservation_service.py
Description: Implements the reservation service for booking tickets, including validation of showtimes and seat availability."""

from decimal import Decimal
from datetime import datetime

from core.ticket import Ticket
from core.seat import Seat
from core.showtime import ShowTime

from storage.json_storage import (
    load_showtimes,
    save_showtimes,
    load_tickets,
    save_tickets,
)

from utils.logger import get_logger

from utils.exceptions import (
    InvalidUserIdError,
    InvalidShowtimeError,
)

logger = get_logger(__name__)




def _check_valid_showtime( showtime_id: str) -> ShowTime:
    showtimes = load_showtimes()

    for showtime_data in showtimes:

        if showtime_data["showtime_id"] == showtime_id:

            showtime = ShowTime.from_dict(showtime_data)

            if showtime.start_time < datetime.now():
                logger.warning(f"Attempt to reserve ticket for past showtime_id='{showtime_id}'")
                raise InvalidShowtimeError(showtime_id)

            logger.debug(f"Valid showtime found for showtime_id='{showtime_id}'")
            return showtime

    logger.error(f"Showtime not found for showtime_id='{showtime_id}'")
    raise InvalidShowtimeError(showtime_id)

def _reserve_seat(
    showtime: ShowTime,
    seat_row: str,
    seat_number: int
    ) -> Seat:

    seat = showtime.get_seat(seat_row, seat_number)

    seat.reserve()

    all_showtimes = load_showtimes()

    for index, showtime_data in enumerate(all_showtimes):

        if showtime_data["showtime_id"] == showtime.showtime_id:

            all_showtimes[index] = showtime.to_dict()

            break

    save_showtimes(all_showtimes)

    logger.info(
        f"Seat '{seat_row}{seat_number}' reserved "
        f"for showtime_id='{showtime.showtime_id}'"
    )

    return seat

def _create_ticket(
    user_id: str,
    showtime_id: str,
    seat_row: str,
    seat_number: int,
    price: Decimal
    ) -> Ticket:

    ticket = Ticket(
        user_id=user_id,
        showtime_id=showtime_id,
        seat_row=seat_row,
        seat_number=seat_number,
        price=price,
        booked_at=datetime.now()
    )

    tickets = load_tickets()
    tickets.append(ticket.to_dict())
    save_tickets(tickets)

    logger.info(
        f"Ticket created for user_id='{user_id}', "
        f"showtime_id='{showtime_id}', "
        f"seat='{seat_row}{seat_number}'"
    )

    return ticket

def reserve_ticket(
    user_id: str,
    showtime_id: str,
    seat_row: str,
    seat_number: int,
    price: Decimal
    ) -> Ticket:

    if not isinstance(user_id, str) or not user_id.strip():
        logger.error(f"Invalid user_id: '{user_id}'")
        raise InvalidUserIdError(user_id)

    showtime = _check_valid_showtime(showtime_id)

    logger.debug(
        f"Attempting to reserve seat '{seat_row}{seat_number}' "
        f"for showtime_id='{showtime_id}' and user_id='{user_id}'"
    )
    _reserve_seat(showtime, seat_row, seat_number)

    ticket = _create_ticket(user_id, showtime_id, seat_row, seat_number, price)

    logger.info(
        f"Ticket reservation successful for user_id='{user_id}', "
        f"showtime_id='{showtime_id}', "
        f"seat='{seat_row}{seat_number}'"
    )
    return ticket
        

        

        

        