"""
Admin service for managing movies and showtimes."""

from core.movie import Movie
from core.showtime import ShowTime

from storage.json_storage import (
    load_movies,
    save_movies,
    load_showtimes,
    save_showtimes,
)

from utils.logger import get_logger

logger = get_logger(__name__)

from utils.exceptions import CinemaTicketError


def add_movie(movie: Movie):
    movies = load_movies()
    movies.append(movie.to_dict())
    save_movies(movies)

    logger.info(f"Added movie: {movie.title}")

def delete_movie(movie_id: str):
    movies = load_movies()

    new_movies = [m for m in movies if m["movie_id"] != movie_id]

    if len(new_movies) == len(movies):
        logger.warning(f"Movie not found: {movie_id}")
        raise CinemaTicketError(f"Movie not found: {movie_id}")

    save_movies(new_movies)

    logger.info(f"Deleted movie with ID: {movie_id}")

def add_showtime(showtime: ShowTime):
    movies = load_movies()
    showtimes = load_showtimes()

    if not any(m["movie_id"] == showtime.movie_id for m in movies):
        raise CinemaTicketError(
            f"Movie does not exist: {showtime.movie_id}"
        )

    showtimes.append(showtime.to_dict())
    save_showtimes(showtimes)

    logger.info(f"Added showtime: {showtime.showtime_id}")

def delete_showtime(showtime_id: str):
    showtimes = load_showtimes()

    new_showtimes = [s for s in showtimes if s["showtime_id"] != showtime_id]

    if len(new_showtimes) == len(showtimes):
        logger.warning(f"Showtime not found: {showtime_id}")
        raise CinemaTicketError(f"Showtime not found: {showtime_id}")

    save_showtimes(new_showtimes)

    logger.info(f"Deleted showtime with ID: {showtime_id}")