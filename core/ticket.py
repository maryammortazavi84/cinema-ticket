"""
Module: ticket.py
Description: Defines the Ticket class representing a ticket for a specific showtime and seat.
"""

from datetime import datetime
from utils.logger import get_logger
from utils.exceptions import (
    InvalidUserIdError,
    InvalidShowtimeError,
    InvalidSeatError)
from decimal import Decimal
from utils.security import generate_unique_id

logger = get_logger(__name__)

class Ticket:
    """Represents a ticket for a specific showtime and seat."""
    def __init__(
                self,
                user_id: str,
                showtime_id: str,
                seat_row: str,
                seat_number: int,
                price: Decimal,
                booked_at: datetime,
                ticket_id: str | None = None
                ):
        
        if not user_id:
            raise InvalidUserIdError(user_id)

        if not showtime_id:
            raise InvalidShowtimeError(showtime_id)

        if not isinstance(seat_row, str) or len(seat_row) != 1:
            raise InvalidSeatError(seat_row)

        if not isinstance(seat_number, int) or seat_number < 1:
            raise InvalidSeatError(seat_number)

        self._ticket_id = ticket_id or generate_unique_id()
        self._user_id = user_id
        self._showtime_id = showtime_id
        self._seat_row = seat_row
        self._seat_number = seat_number
        self._price = price
        self._booked_at = booked_at or datetime.now()

    # only read properties
    @property
    def ticket_id(self) -> str:
        return self._ticket_id
    
    @property
    def user_id(self) -> str:
        return self._user_id
    
    @property
    def showtime_id(self) -> str:
        return self._showtime_id
    
    @property
    def seat_row(self) -> str:
        return self._seat_row
    
    @property
    def seat_number(self) -> int:
        return self._seat_number
    
    @property
    def price(self) -> Decimal:
        return self._price
    
    @property
    def booked_at(self) -> datetime:
        return self._booked_at

    def to_dict(self) -> dict:
        """Convert the Ticket instance to a dictionary."""
        return {
            "ticket_id": self.ticket_id,
            "user_id": self.user_id,
            "showtime_id": self.showtime_id,
            "seat_row": self.seat_row,
            "seat_number": self.seat_number,
            "price": str(self.price),  # Convert Decimal to string for JSON serialization
            "booked_at": self.booked_at.isoformat()  # Convert datetime to ISO format string
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Ticket':
        """Create a Ticket instance from a dictionary."""
        return cls(
            ticket_id=data.get("ticket_id"),
            user_id=data["user_id"],
            showtime_id=data["showtime_id"],
            seat_row=data["seat_row"],
            seat_number=data["seat_number"],
            price=Decimal(data["price"]),  # Convert string back to Decimal
            booked_at=datetime.fromisoformat(data["booked_at"])  # Convert ISO format string back to datetime
        )
    
    def __str__(self) -> str:
        return (f"Ticket(ticket_id={self.ticket_id}, user_id={self.user_id}, "
                f"showtime_id={self.showtime_id}, seat_row={self.seat_row}, "
                f"seat_number={self.seat_number}, price={self.price}, "
                f"booked_at={self.booked_at.isoformat()})")