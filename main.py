import argparse
from getpass import getpass

from user_script import user_menu
from admin_script import admin_menu

from utils.console import print_error, print_success
from utils.logger import get_logger

logger = get_logger(__name__)

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"


def admin_login():
    username = input("Admin Username: ")
    password = getpass("Admin Password: ")

    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        logger.info("Admin logged in successfully.")
        print_success("Admin login successful!")
        input("Press Enter to continue...")
        admin_menu()
    else:
        logger.warning("Failed admin login attempt.")
        print_error("Invalid admin credentials.")
        input("Press Enter to continue...")


def main():
    parser = argparse.ArgumentParser(
        description="Cinema Ticket System"
    )

    parser.add_argument(
        "--admin",
        action="store_true",
        help="Run admin panel"
    )

    args = parser.parse_args()

    if args.admin:
        admin_login()
    else:
        user_menu()


if __name__ == "__main__":
    main()