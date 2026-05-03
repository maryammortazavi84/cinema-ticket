""""""
from utils.logger import get_logger
from utils.exceptions import (
    InvalidSeatRowError,
    InvalidSeatNumberError,
    SeatAlreadyReservedError,
    SeatAlreadyAvailableError
)

logger = get_logger(__name__)

class Seat:
    def __init__(self, row: str, number: int):
        """Initialize a Seat instance."""
        self.row = row
        self.number = number
        self.is_available: bool = True  # By default, the seat is available

    #row
    @property
    def row(self) -> str:
        return self._row
    
    @row.setter
    def row(self, value: str) -> None:
        if not isinstance(value, str):
            logger.error(f"Invalid seat row type: {value} (type: {type(value)}). Expected a string.")
            raise InvalidSeatRowError(value)
        value = value.strip().upper()
        if not value or len(value) > 1 or not 'A' <= value <= 'Z':
            logger.error(f"Invalid seat row value: '{value}'. Expected a single letter from A to Z.")   
            raise InvalidSeatRowError(value)
        self._row = value

    #number
    @property
    def number(self) -> int:
        return self._number

    @number.setter
    def number(self, value: int) -> None:
        if not isinstance(value, int):
            logger.error(f"Invalid seat number type: {value} (type: {type(value)}). Expected an integer.")
            raise InvalidSeatNumberError(value)
        if not 1 <= value <= 40:
            logger.error(f"Invalid seat number value: {value}. Expected an integer between 1 and 40.")
            raise InvalidSeatNumberError(value)
        self._number = value

    def reserve(self) -> None:
        """Reserve the seat if it is available."""
        if not self.is_available:
            logger.warning(f"Attempted to reserve seat {self.row}{self.number}, but it is already reserved.")
            raise SeatAlreadyReservedError(seat_number=f"{self.row}{self.number}")
        self.is_available = False
        logger.info(f"Seat {self.row}{self.number} has been reserved.")

    def release(self) -> None:
        """Release the seat, making it available again."""
        if self.is_available:
            logger.warning(f"Attempted to release seat {self.row}{self.number}, but it is already available.")
            raise SeatAlreadyAvailableError(seat_number=f"{self.row}{self.number}")
        self.is_available = True
        logger.info(f"Seat {self.row}{self.number} has been released and is now available.")

    def to_dict(self) -> dict:
        """Convert the Seat instance to a dictionary representation."""
        return {
            "row": self.row,
            "number": self.number,
            "is_available": self.is_available
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create a Seat instance from a dictionary representation."""
        seat = cls(row=data["row"], number=data["number"])
        seat.is_available = data.get("is_available", True)
        return seat

    def __str__(self):
        status = "Available" if self.is_available else "Reserved"
        return f"Seat {self.row}{self.number} - {status}"