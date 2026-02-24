"""
Movie class representing a movie in the cinema ticket booking system.
This class includes attributes for movie details such as title, duration, age rating, and genre.
It also includes validation for these attributes and methods for converting to/from dictionary representations.
The Movie class is designed to be used in conjunction with the movie management service and the JSON storage layer for persistence.
"""
from core.enums import AgeRating
from utils.exceptions import (
    InvalidAgeRatingError,
    InvalidDurationError,
    InvalidMovieTitleError,
    InvalidGenreError
)
from utils.security import generate_unique_id
from utils.logger import get_logger
logger = get_logger(__name__)


class Movie:
    def __init__(self,
                 title: str,
                duration_minutes: int,
                age_rating: AgeRating,
                genre: str,
                movie_id: str | None = None
                ):
        """Initialize a new Movie instance.
        Args:
            title: The title of the movie (non-empty string).
            duration_minutes: The duration of the movie in minutes (positive integer).
            age_rating: The age rating of the movie (must be a valid AgeRating enum value).
            genre: The genre of the movie (non-empty string).
            movie_id: Optional unique identifier for the movie (auto-generated if not provided)."""
        self._movie_id = generate_unique_id() if not movie_id else movie_id
        self.title = title
        self.duration_minutes = duration_minutes
        self.age_rating = age_rating
        self.genre = genre

    #read only

    @property
    def movie_id(self) -> str:
        return self._movie_id
    
    #title
    @property
    def title(self) -> str:
        return self._title
    
    @title.setter
    def title(self, value: str) -> None:
        if not isinstance(value, str):
            raise InvalidMovieTitleError(value)
        value = value.strip()
        if not value:
            raise InvalidMovieTitleError(value)
        self._title = value

    #duration
    @property
    def duration_minutes(self) -> int:
        return self._duration_minutes
    
    @duration_minutes.setter
    def duration_minutes(self, value: int) -> None:
        if not isinstance(value, int) or value <= 0:
            raise InvalidDurationError(value)
        self._duration_minutes = value

    #age rating
    @property
    def age_rating(self) -> AgeRating:
        return self._age_rating
    
    @age_rating.setter
    def age_rating(self, value: AgeRating) -> None:
        if not isinstance(value, AgeRating):
            raise InvalidAgeRatingError(value)
        self._age_rating = value

    #genre
    @property
    def genre(self) -> str:
        return self._genre
    
    @genre.setter
    def genre(self, value: str) -> None:
        if not isinstance(value, str):
            raise InvalidGenreError()
        value = value.strip()
        if not value:
            raise InvalidGenreError()
        self._genre = value

    def __str__(self):
        return f"Movie(id={self.movie_id}, title='{self.title}', duration={self.duration_minutes} mins, age_rating={self.age_rating}, genre='{self.genre}')"
    
    def to_dict(self) -> dict:
        """Convert the Movie instance to a dictionary for serialization."""
        return {
            "movie_id": self.movie_id,
            "title": self.title,
            "duration_minutes": self.duration_minutes,
            "age_rating": self.age_rating.value,
            "genre": self.genre
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create a Movie instance from a dictionary."""
        return cls(
            movie_id=data["movie_id"],
            title=data["title"],
            duration_minutes=data["duration_minutes"],
            age_rating=AgeRating(data["age_rating"]),
            genre=data["genre"]
        )

    