"""
Movie Service Module
This module provides services for managing movies, including adding new movies, retrieving movies by ID, searching for movies by title, and deleting movies. It interacts with the Movie class from the core module and uses JSON storage for persistence.
The service functions include:
- add_movie: Adds a new movie to the collection with validation for input parameters.
- get_all_movies: Retrieves all movies from the collection.
- get_movie_by_id: Retrieves a specific movie by its unique identifier, raising an error if not found.
- search_movies_by_title: Searches for movies by title using a case-insensitive substring match.
- delete_movie: Deletes a movie by its unique identifier, raising an error if not found.
The module also includes logging for all operations to facilitate debugging and monitoring of movie management activities."""

from core.movie import Movie
from storage.json_storage import load_movies, save_movies
from utils.exceptions import MovieNotFoundError
from core.enums import AgeRating
from utils.logger import get_logger

logger = get_logger(__name__)

def add_movie(title: str,
              duration_minutes: int,
              age_rating: AgeRating,
              genre: str) -> Movie:
    """Add a new movie to the collection.
    Args:   
        title: The title of the movie (non-empty string).
        duration_minutes: The duration of the movie in minutes (positive integer).
        age_rating: The age rating of the movie (must be a valid AgeRating enum value).
        genre: The genre of the movie (non-empty string).
    Returns:
        The newly added Movie instance."""
    logger.info(f"Adding new movie: {title}")
    try:
        movie = Movie(title=title, duration_minutes=duration_minutes, age_rating=age_rating, genre=genre)
    except Exception as e:
        logger.error(f"Failed to save movie '{title}': {e}", exc_info=True)
        raise
    movies = load_movies()
    movies.append(movie.to_dict())
    save_movies(movies)
    return movie


def get_all_movies() -> list[Movie]:
    """Retrieve all movies from the collection.
    Returns:
        A list of Movie instances representing all movies in the collection."""
    logger.info("Retrieving all movies")
    try:
        movies_data = load_movies()
        logger.info(f"Retrieved {len(movies_data)} movies") 
        return [Movie.from_dict(movie_data) for movie_data in movies_data]
    except Exception as e:
        logger.error(f"Failed to retrieve movies: {e}", exc_info=True)
        raise

def get_movie_by_id(movie_id: str) -> Movie:
    """Retrieve a movie by its unique identifier.
    Args:
        movie_id: The unique identifier of the movie to retrieve.
    Returns:
        The Movie instance with the specified movie_id.
    Raises:
        MovieNotFoundError: If no movie with the specified movie_id is found."""
    logger.info(f"Retrieving movie with ID: {movie_id}")
    movies = load_movies()
    for movie_data in movies:
        if movie_data.get("movie_id") == movie_id:
            return Movie.from_dict(movie_data)
    logger.warning(f"Movie with ID '{movie_id}' not found")
    raise MovieNotFoundError(movie_id)

def search_movies_by_title(title: str) -> list[Movie]:
    """Search for movies by title.
    Args:
        title: The title to search for (case-insensitive substring match).
    Returns:
        A list of Movie instances matching the search criteria."""
    logger.info(f"Searching for movies with title: {title}")
    movies = load_movies()
    return [Movie.from_dict(movie_data) for movie_data in movies if title.strip().lower() in movie_data.get("title", "").lower()]

def delete_movie(movie_id: str) -> None:
    """Delete a movie by its unique identifier.
    Args:
        movie_id: The unique identifier of the movie to delete.
    Raises:
        MovieNotFoundError: If no movie with the specified movie_id is found."""
    logger.info(f"Deleting movie with ID: {movie_id}")
    movies = load_movies()
    for i, movie_data in enumerate(movies):
        if movie_data.get("movie_id") == movie_id:
            del movies[i]
            save_movies(movies)
            logger.info(f"Movie with ID '{movie_id}' deleted successfully")
            return
    logger.warning(f"Movie with ID '{movie_id}' not found for deletion")
    raise MovieNotFoundError(movie_id)