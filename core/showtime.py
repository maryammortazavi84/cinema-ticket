"""
This module defines the ShowTime class, which represents a specific screening of a movie at a given time and location.
The ShowTime class includes attributes for movie ID, start time, hall name, and a list of Seat objects representing the seating arrangement for that showtime.
It also includes methods for retrieving available seats, converting to/from dictionary format for storage, and string representation for easy debugging and display.
The ShowTime class includes validation for its attributes and raises custom exceptions for invalid data."""
from datetime import datetime
from core.seat import Seat
from utils.security import generate_unique_id
from utils.logger import get_logger
from utils.exceptions import (
    InvalidShowtimeError,
    InvalidHallNameError,
    InvalidMovieIdError,
    InvalidSeatError,
)
from decimal import Decimal

logger = get_logger(__name__)

class ShowTime:
    
    def __init__(
        self,
        movie_id: str,
        start_time: datetime,
        hall_name: str,
        price: Decimal,
        showtime_id: str | None = None
        ):
        """Initializes a ShowTime instance with validation and logging.
         - Validates movie_id, start_time, and hall_name using property setters.
         - Generates a unique showtime_id if not provided.
         - Logs the creation process for debugging purposes.
        """
        logger.debug(f"Creating showtime for movie_id='{movie_id}', start_time='{start_time}', hall_name='{hall_name}'")
        # immutable
        self._showtime_id = generate_unique_id() if showtime_id is None else showtime_id
        # validated fields via setters
        self.movie_id = movie_id
        self.start_time = start_time
        self.hall_name = hall_name
        self.seats: list[Seat] = self._generate_seats()
        self.price = Decimal(str(price))

    @property
    def showtime_id(self) -> str:
        return self._showtime_id

    # movie_id
    @property
    def movie_id(self) -> str:
        return self._movie_id
    @movie_id.setter
    def movie_id(self, value: str) -> None:
        if not isinstance(value, str):
            raise InvalidMovieIdError(value)    
        value = value.strip()
        if not value:
            raise InvalidMovieIdError(value)
        self._movie_id = value

    # start_time
    @property
    def start_time(self) -> datetime:
        return self._start_time
    @start_time.setter
    def start_time(self, value: datetime) -> None:
        if not isinstance(value, datetime):
            raise InvalidShowtimeError(value)
        self._start_time = value

    # hall_name
    @property
    def hall_name(self) -> str:
        return self._hall_name
    @hall_name.setter
    def hall_name(self, value: str) -> None:
        if not isinstance(value, str):
            raise InvalidHallNameError(value)
        value = value.strip()
        if not value:
            raise InvalidHallNameError(value)
        self._hall_name = value

    @property
    def price(self) -> Decimal:
        return self._price
    @price.setter
    def price(self, value: Decimal) -> None:
        if not isinstance(value, Decimal) or value < Decimal("0.00"):
            raise ValueError(f"Invalid price: {value}")
        self._price = value

    # seats are generated based on hall configuration, so no setter for seats
    def _generate_seats(self) -> list[Seat]:
        # For simplicity, we assume each hall has 5 rows (A-E) and 10 seats per row (1-10)
        seats = []
        for row in ['A', 'B', 'C', 'D', 'E']:
            for number in range(1, 11):
                seats.append(Seat(row, number))
        return seats
    
    def get_seat(self, row: str, number: int) -> Seat:
        """Returns the Seat object for the given row and number."""
        for seat in self.seats:
            if seat.row == row and seat.number == number:
                return seat
        raise InvalidSeatError(f"{row}{number}")
    
    def get_available_seats(self) -> list[Seat]:
        """Returns a list of available seats for this showtime."""
        return [seat for seat in self.seats if seat.is_available]
    
    def to_dict(self) -> dict:
        """Converts the ShowTime instance to a dictionary for storage."""
        return {
            "showtime_id": self.showtime_id,
            "movie_id": self.movie_id,
            "start_time": self.start_time.isoformat(),
            "hall_name": self.hall_name,
            "seats": [seat.to_dict() for seat in self.seats],
            "price": str(self.price)
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Creates a ShowTime instance from a dictionary."""
        showtime = cls(
            movie_id=data["movie_id"],
            start_time=datetime.fromisoformat(data["start_time"]),
            hall_name=data["hall_name"],
            showtime_id=data["showtime_id"],
            price=Decimal(str(data["price"]))
        )
        showtime.seats = [Seat.from_dict(seat_data) for seat_data in data.get("seats", [])]
        return showtime
    
    def __str__(self):
        return (
            f"Showtime ID: {self.showtime_id}\n"
            f"Movie ID: {self.movie_id}\n"
            f"Start Time: {self.start_time}\n"
            f"Hall Name: {self.hall_name}\n"
            f"Available Seats: {len(self.get_available_seats())}/{len(self.seats)}\n"
            f"Price: ${self.price}"
        )