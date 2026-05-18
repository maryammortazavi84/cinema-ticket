"""
Admin script for managing movies and showtimes.
This script provides a command-line interface for administrators to add and delete movies and showtimes.
It interacts with the admin service layer to perform these operations and uses the console utilities for user input
"""

from datetime import datetime
from decimal import Decimal

from core.enums import AgeRating

from core.movie import Movie
from core.showtime import ShowTime

from services.admin_service import (
    add_movie,
    delete_movie,
    add_showtime,
    delete_showtime,
)

from storage.json_storage import (
    load_movies,
    load_showtimes,
)

from utils.console import (
    print_menu,
    get_choice,
    get_input,
    print_success,
    print_error,
    print_info,
)

from utils.exceptions import CinemaTicketError

from utils.logger import get_logger

logger = get_logger(__name__)


def admin_menu():
    while True:
        print_menu(
            [
                "Add Movie",
                "Delete Movie",
                "Add ShowTime",
                "Delete ShowTime",
                "Back to Main Menu",
            ],
            title="Admin Menu"
        )

        choice = get_choice(5)

        if choice == 1:
            add_movie_flow()
        elif choice == 2:
            delete_movie_flow()
        elif choice == 3:
            add_showtime_flow()
        elif choice == 4:
            delete_showtime_flow()
        else:
            break


def add_movie_flow():
    title = get_input("Movie Title: ")
    duration_str = get_input("Duration (minutes): ")
    age_rating_str = get_input("Age Rating (G, PG, PG13, R, NC-17): ")
    genre = get_input("Genre: ")

    try:
        duration = int(duration_str)
        if duration <= 0:
            raise ValueError()

    except ValueError:
        logger.exception(f"Invalid duration input: {duration_str}")
        print_error("Duration must be a positive integer!")
        input("Press Enter to continue...")
        return

    try:
        age_rating = AgeRating[age_rating_str.upper()]

    except KeyError:
        logger.error(f"Invalid age rating input: {age_rating_str}")
        print_error("Invalid age rating!")
        input("Press Enter to continue...")
        return

    try:
        movie = Movie(
            title=title,
            duration_minutes=duration,
            age_rating=age_rating,
            genre=genre
        )

        add_movie(movie)

        logger.info(f"Movie added: {title}")

        print_success(f"Movie '{title}' added successfully!")
        input("Press Enter to continue...")

    except CinemaTicketError as e:
        logger.exception(f"Error adding movie: {e}")

        print_error(str(e))
        input("Press Enter to continue...")

        return


def delete_movie_flow():
    movies = load_movies()

    if not movies:
        print_info("No movies available to delete.")
        input("Press Enter to continue...")
        return

    print_menu(
        [f"{m['title']} (ID: {m['movie_id']})" for m in movies],
        title="Select Movie to Delete"
    )

    choice = get_choice(len(movies))
    movie_id = movies[choice - 1]["movie_id"]

    try:
        delete_movie(movie_id)

        logger.info(f"Movie deleted: {movie_id}")

        print_success("Movie deleted successfully!")
        input("Press Enter to continue...")

    except CinemaTicketError as e:
        logger.exception(f"Error deleting movie: {e}")

        print_error(str(e))
        input("Press Enter to continue...")


def add_showtime_flow():
    movies = load_movies()

    if not movies:
        print_info("No movies available. Please add a movie first.")
        input("Press Enter to continue...")
        return

    print_menu(
        [f"{m['title']} (ID: {m['movie_id']})" for m in movies],
        title="Select Movie for Showtime"
    )

    choice = get_choice(len(movies))
    movie_id = movies[choice - 1]["movie_id"]

    datetime_str = get_input("Showtime (YYYY-MM-DD HH:MM): ")
    hall_name = get_input("Hall name: ")

    try:
        start_time = datetime.strptime(
            datetime_str,
            "%Y-%m-%d %H:%M"
        )

    except ValueError:
        logger.error(f"Invalid datetime input: {datetime_str}")

        print_error("Invalid datetime format!")
        input("Press Enter to continue...")

        return

    try:
        showtime = ShowTime(
            movie_id=movie_id,
            start_time=start_time,
            hall_name=hall_name,
            price=Decimal("10.00")
        )

        add_showtime(showtime)

        logger.info(f"Showtime added for movie ID: {movie_id}")

        print_success("Showtime added successfully!")
        input("Press Enter to continue...")

    except CinemaTicketError as e:
        logger.exception(f"Error adding showtime: {e}")

        print_error(str(e))
        input("Press Enter to continue...")


def delete_showtime_flow():
    showtimes = load_showtimes()

    if not showtimes:
        print_info("No showtimes available to delete.")
        input("Press Enter to continue...")
        return

    print_menu(
        [
            f"{s['movie_id']} at "
            f"{datetime.fromisoformat(s['start_time']).strftime('%Y-%m-%d %H:%M')} "
            f"(ID: {s['showtime_id']})"
            for s in showtimes
        ],
        title="Select Showtime to Delete"
    )

    choice = get_choice(len(showtimes))
    showtime_id = showtimes[choice - 1]["showtime_id"]

    try:
        delete_showtime(showtime_id)

        logger.info(f"Showtime deleted: {showtime_id}")

        print_success("Showtime deleted successfully!")
        input("Press Enter to continue...")

    except CinemaTicketError as e:
        logger.exception(f"Error deleting showtime: {e}")

        print_error(str(e))
        input("Press Enter to continue...")