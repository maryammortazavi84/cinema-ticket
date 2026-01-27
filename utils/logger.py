"""
Logger configuration for the Cinema Ticket project.
All events should be logged using the get_logger() function.
Logs are saved to logs/cinematicket.log
"""

import logging
from storage.file_paths import LOG_FILE





def get_logger(name: str = "CinemaTicket") -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.hasHandlers():
        return logger
    

    logger.setLevel(logging.INFO)

    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(name)s - %(funcName)s:%(lineno)d - %(message)s"
    DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)

    streamhandler = logging.StreamHandler()
    streamhandler.setLevel(logging.ERROR)
    streamhandler.setFormatter(formatter)
    logger.addHandler(streamhandler)

    filehandler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    filehandler.setLevel(logging.INFO)
    filehandler.setFormatter(formatter)
    logger.addHandler(filehandler)

    logger.propagate = False


    return logger



