"""
JSON storage layer for Cinema Ticket project.

Users structure:

{
    "by_id": {
        "user_id": {user_data}
    },
    "username_index": {
        "username": "user_id"
    }
}

This structure allows:
- Fast lookup by ID
- O(1) lookup by username using index
"""

import json
from storage.file_paths import (
    USERS_FILE,
    SHOWTIMES_FILE,
    TICKETS_FILE,
    MOVIES_FILE,
)
from pathlib import Path
from utils.logger import get_logger 
from utils.exceptions import CinemaTicketError
from typing import Any

logger = get_logger(__name__)

def load_data(file_path: Path, default: Any):
    """ Loads data from a JSON file."""

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
        
    except FileNotFoundError:
        logger.warning(f"File {file_path} not found. Returning default.")
        return default

    except json.JSONDecodeError:
        logger.error(f"Corrupted JSON in {file_path}. Returning default.")
        return default
    

def save_data(file_path: Path, data: list|dict) ->None:
    """ Saves data to a JSON file."""
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        logger.info(f"File {file_path} saved successfully")

    except OSError as e:
        logger.error(f"Failed to save file {file_path}\nDetails: {e}", exc_info=True)
        raise CinemaTicketError("Storage error: failed to save data") from e
    
# =====================
# Domain-specific helpers
# =====================

DEFAULT_USERS_STRUCTURE = {
    "by_id": {},
    "username_index": {}
}


def load_users() -> dict:
    """
    Returns users data with structure:
    {
        "by_id": {...},
        "username_index": {...}
    }
    """
    data = load_data(USERS_FILE, DEFAULT_USERS_STRUCTURE)

    if "by_id" not in data:
        data["by_id"] = {}

    if "username_index" not in data:
        data["username_index"] = {}

    return data

def save_users(users: dict) -> None:
    """Saves users dict with user_id as key"""
    return save_data(USERS_FILE, users)

def load_showtimes() -> list:
    return load_data(SHOWTIMES_FILE, [])

def save_showtimes(showtimes: list) -> None:
    return save_data(SHOWTIMES_FILE, showtimes)

def load_tickets() -> list:
    return load_data(TICKETS_FILE, [])

def save_tickets(tickets: list) -> None:
    return save_data(TICKETS_FILE, tickets)

def load_movies() -> list:
    return load_data(MOVIES_FILE, [])

def save_movies(movies: list) -> None:
    return save_data(MOVIES_FILE, movies)


        
    

    

