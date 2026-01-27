"""
Centralized file paths for the Cinema Ticket project.

This module defines all file and directory paths used throughout the project.
All other modules should import paths from here to ensure consistency and easy maintenance.
"""
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.resolve()

DATA_DIR = BASE_DIR/ "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

LOGS_DIR = BASE_DIR/ "logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True)

USERS_FILE = DATA_DIR/ "users.json"
SHOWTIMES_FILE = DATA_DIR/ "showtimes.json"
TICKETS_FILE = DATA_DIR/ "tickets.json"
MOVIES_FILE = DATA_DIR/ "movies.json"
WALLETS_FILE = DATA_DIR/ "wallets.json"

LOG_FILE = LOGS_DIR/ "cinematicket.log"