"""
This module contains the user-facing console application logic. It provides a menu-driven interface for users to interact with the cinema ticketing system. Users can register, log in, view movies and showtimes, reserve tickets, manage their wallet, and handle subscriptions. The module interacts with the service layer to perform these operations and uses console utilities for input/output.
The user script is designed to be intuitive and user-friendly, guiding users through various functionalities of the system while ensuring proper error handling and logging for a smooth experience.
"""

from datetime import datetime
from decimal import Decimal
from getpass import getpass

from core.enums import SubscriptionType
from services.auth_service import register_user, login_user

from services.user_service import (
    change_username,
    change_phone,
    change_password,
    get_user_profile
)

from services.subscription_service import (
    get_user_subscription,
    get_user_subscription_type,
    create_subscription,
    apply_subscription_benefits
)

from core.enums import AgeRating

from services.reservation_service import reserve_ticket

from services.gateway_service import Gateway_service, Gateway

from storage.json_storage import load_movies, load_showtimes, load_tickets, load_users, save_users



from utils.console import (
    print_menu,
    get_choice,
    get_input,
    print_success,
    print_error,
    print_info,
)

from utils.logger import get_logger
from utils.exceptions import CinemaTicketError, InvalidAmountError

logger = get_logger(__name__)


def user_menu():
    while True:
        print_menu(
            [
                "Register",
                "Login",
                "Exit"
            ],
            title="User Menu"
        )

        choice = get_choice(3)

        if choice == 1:
            register_flow()
        elif choice == 2:
            login_flow()
        else:
            break

# _____________________________________________registration and login flows_____________________________________________
def register_flow():
    print_info("Register a new account")
    input("Press Enter to continue...")

    username = get_input("Username: ")
    birth_date = get_input("Birth date (YYYY-MM-DD): ")
    phone = get_input("Phone (optional): ", required=False)
    password = getpass("Password: ")

    try:
        register_user(username, password, birth_date, phone)
        logger.info(f"User registered: {username}")
        print_success("Registration successful! You can now log in.")
        input("Press Enter to continue...")
    except CinemaTicketError as e:
        logger.exception(f"Error registering user: {e}")
        print_error(str(e))
        input("Press Enter to continue...")


def login_flow():
    print_info("Login to your account")
    input("Press Enter to continue...")

    username = get_input("Username: ")
    password = getpass("Password: ")

    try:
        user = login_user(username, password)
        logger.info(f"User logged in: {username}")
        print_success(f"Welcome back, {username}!")
        input("Press Enter to continue...")
        user_profile_menu(user)
    except CinemaTicketError as e:
        logger.exception(f"Error logging in: {e}")
        print_error(str(e))
        input("Press Enter to continue...")


# ___________________________________________user profile______________________________________________________________
def user_profile_menu(user):
    while True:
        print_menu(
            [
                "Movies & Showtimes",
                "Tickets (Reserve / View)",
                "Wallet",
                "Subscription",
                "Profile",
                "Logout"
            ],
            title="Profile Menu"
        )

        choice = get_choice(6)
        if choice == 1:
            movies_showtimes_flow()
            input("Press Enter to continue...")
        elif choice == 2:
            tickets_flow(user)
        elif choice == 3:
            wallet_flow(user)
        elif choice == 4:
            subscription_flow(user)
        elif choice == 5:
            profile_flow(user)
        else:
            break


# ___________________________________________movies and showtimes____________________________________________________

def movies_showtimes_flow():
    movies = load_movies()
    showtimes = load_showtimes()

    if not movies:
        print_info("No movies available at the moment.")
        input("Press Enter to continue...")
        return

    print_info("Available Movies and Showtimes:")
    input("Press Enter to continue...")

    for m in movies:
        print(f"{m['title']} ({m['genre']}, {m['duration_minutes']} mins, {m['age_rating']})")

        for s in showtimes:
            if s["movie_id"] == m["movie_id"]:
                start_time = datetime.fromisoformat(s["start_time"])
                formatted_time = start_time.strftime("%Y-%m-%d %H:%M")

                print(f"  - {formatted_time} (Showtime ID: {s['showtime_id']})")

# ___________________________________________tickets (reserve / view)____________________________________________________
def tickets_flow(user):
    while True:
        print_menu(
            [
                "Reserve Ticket",
                "My Tickets",
                "Back"
            ],
            title="Tickets Menu"
        )

        choice = get_choice(3)

        if choice == 1:
            reserve_ticket_flow(user)
        elif choice == 2:
            view_tickets_flow(user)
        else:
            break


def reserve_ticket_flow(user):
    movies = load_movies()
    if not movies:
        print_info("No movies available at the moment.")
        input("Press Enter to continue...")
        return

    print_menu(
        [f"{m['title']} ({m['genre']}, {m['duration_minutes']} mins, {m['age_rating']})" for m in movies],
        title="Select Movie"
    )
    movie_choice = get_choice(len(movies))
    selected_movie = movies[movie_choice - 1]
    movie_id = selected_movie["movie_id"]

    showtimes = load_showtimes()
    movie_showtimes = [s for s in showtimes if s["movie_id"] == movie_id]

    if not movie_showtimes:
        print_info("No showtimes available for this movie.")
        input("Press Enter to continue...")
        return

    print_menu(
        [f"{datetime.fromisoformat(s['start_time']).strftime('%Y-%m-%d %H:%M')} (Hall: {s['hall_name']}, Price: ${s['price']})" for s in movie_showtimes],
        title="Select Showtime"
    )
    showtime_choice = get_choice(len(movie_showtimes))
    selected_showtime = movie_showtimes[showtime_choice - 1]

    seats = selected_showtime["seats"]
    available_seats = [s for s in seats if s.get("is_available", False)]

    if not available_seats:
        print_info("No seats available for this showtime.")
        input("Press Enter to continue...")
        return

    print_menu(
        [f"{s['row']}{s['number']}" for s in available_seats],
        title="Select Seat"
    )
    seat_choice = get_choice(len(available_seats))
    selected_seat = available_seats[seat_choice - 1]

    price = apply_subscription_benefits(
    user,
    Decimal(selected_showtime["price"])
    )
    print_info(f"Selected seat: {selected_seat['row']}{selected_seat['number']} - Price: ${price}")
    input("Press Enter to continue...")

    age_rating = AgeRating(selected_movie["age_rating"])
    if user.age < age_rating.min_age:
        print_error("You are not allowed to watch this movie.")
        input("Press Enter to continue...")
        return

    gateway = Gateway(gateway_id="default_gateway")
    gateway_service = Gateway_service(gateway)

    try:
        gateway_service.withdraw_from_wallet(price,
                                             user,
                                             description=f"Ticket for {selected_movie['title']} at {selected_showtime['start_time']}"
                                             )

        data = load_users()
        data["by_id"][user.id] = user.to_dict()
        save_users(data)

        reserve_ticket(user.id, selected_showtime["showtime_id"], selected_seat["row"], selected_seat["number"], price)
        logger.info(f"Ticket reserved for user_id: {user.id}, showtime_id: {selected_showtime['showtime_id']}, seat: {selected_seat['row']}{selected_seat['number']}")
        print_success("Ticket reserved successfully!")
        input("Press Enter to continue...")

    except CinemaTicketError as e:
        logger.exception(f"Error reserving ticket: {e}")
        print_error(str(e))
        input("Press Enter to continue...")


def view_tickets_flow(user):
    tickets = load_tickets()
    showtimes = load_showtimes()
    movies = load_movies()

    user_tickets = [t for t in tickets if t["user_id"] == user.id]

    if not user_tickets:
        print_info("You have no tickets.")
        input("Press Enter to continue...")
        return

    print_info("Your Tickets:")
    input("Press Enter to continue...")

    for t in user_tickets:
        showtime = next(
            (s for s in showtimes if s["showtime_id"] == t["showtime_id"]),
            None
        )

        if not showtime:
            movie_title = "Unknown Movie"
            start_time = "Unknown Time"
        else:
            movie = next(
                (m for m in movies if m["movie_id"] == showtime["movie_id"]),
                None
            )
            movie_title = movie["title"] if movie else "Unknown Movie"
            start_time = datetime.fromisoformat(showtime["start_time"]).strftime("%Y-%m-%d %H:%M")

        print(
            f"- {movie_title} at {start_time}, "
            f"Seat: {t['seat_row']}{t['seat_number']} "
            f"(Ticket ID: {t['ticket_id']})"
        )
        input("Press Enter to continue...")

# ___________________________________________Wallet______________________________________________________________

def wallet_flow(user):
    while True:
        print_menu(
            [
                "View Balance",
                "Deposit",
                "Back"
            ],
            title="Wallet Menu"
        )
        choice = get_choice(3)

        if choice == 1:
            print_info(f"Current Balance: ${user.wallet_balance:.2f}")
            input("Press Enter to continue...")

        elif choice == 2:
            amount_str = get_input("Amount to deposit: $")

            try:
                amount = Decimal(amount_str)

                if amount <= 0:
                    logger.error(f"Invalid deposit amount: {amount} for user_id: {user.id}")
                    print_error("Amount must be positive!")
                    input("Press Enter to continue...")
                    raise InvalidAmountError(amount)

                gateway = Gateway(gateway_id="default_gateway")
                gateway_service = Gateway_service(gateway)

                result = gateway_service.deposit_to_wallet(
                    amount,
                    user,
                    description="Wallet Deposit"
                )

                if result:
                    data = load_users()
                    data["by_id"][user.id] = user.to_dict()
                    save_users(data)

                    logger.info(f"Deposited ${amount} to wallet for user_id: {user.id}")
                    print_success(f"Deposited ${amount} successfully!")
                    
                else:
                    print_error("Deposit failed!")

                input("Press Enter to continue...")

            except InvalidAmountError:
                logger.error(f"Invalid deposit amount for user_id: {user.id}")
                print_error("Amount must be positive!")
                input("Press Enter to continue...")

            except Exception as e:
                logger.exception(f"Error depositing to wallet: {e}")
                print_error("Something went wrong!")
                input("Press Enter to continue...")

        else:
            break
# ______________________________________Subscription______________________________________________________________
def subscription_flow(user):
    while True:
        print_menu(
            [
                "View Subscription",
                "Subscribe / Upgrade",
                "View Benefits",
                "Back"
            ],
            title="Subscription Menu"
        )

        choice = get_choice(4)

        if choice == 1:
            sub = get_user_subscription(user.id)

            if not sub:
                print_info(
                    "Type: BRONZE (default)\n"
                    "Start: N/A\n"
                    "End: N/A\n"
                    "Active: True"
                )
                input("Press Enter to continue...")
                continue

            print_info(
                f"Type: {sub.subscription_type.value}\n"
                f"Start: {sub.start_date}\n"
                f"End: {sub.end_date}\n"
                f"Active: {sub.is_active()}"
            )
            input("Press Enter to continue...")

        elif choice == 2:
            create_subscription_flow(user)

        elif choice == 3:
            sub = get_user_subscription(user.id)
            sub_type = SubscriptionType.BRONZE if sub is None else sub.subscription_type

            if sub_type == SubscriptionType.BRONZE:
                print_info("Bronze plan: no benefits available.")
                input("Press Enter to continue...")
                continue

            if sub is None:
                print_info("Subscription data not found.")
                input("Press Enter to continue...")
                continue

            if sub_type == SubscriptionType.SILVER:
                print_info(
                    "Silver Benefits:\n"
                    "- 20% cashback\n"
                    f"- Remaining credits: {sub.remaining_credits}"
                )
                input("Press Enter to continue...")

            elif sub_type == SubscriptionType.GOLD:
                print_info(
                    "Gold Benefits:\n"
                    "- 50% discount\n"
                    f"- Drink credits: {sub.apply_gold_drink_benefits}"
                )
                input("Press Enter to continue...")

        else:
            break


def create_subscription_flow(user):
    print_menu(
        [
            "Silver (20% cashback + 3 credits)",
            "Gold (50% discount + drinks)"
        ],
        title="Choose Subscription Plan"
    )

    choice = get_choice(2)

    try:
        if choice == 1:
            sub_type = SubscriptionType.SILVER

        elif choice == 2:
            sub_type = SubscriptionType.GOLD

        else:
            sub_type = SubscriptionType.BRONZE

        sub = create_subscription(user.id, sub_type)

        logger.info(f"Subscription created: {user.id} -> {sub_type.value}")
        print_success(f"{sub_type.value.capitalize()} subscription activated!")
        input("Press Enter to continue...")

    except Exception as e:
        logger.exception(f"Subscription creation failed: {e}")
        print_error(str(e))
        input("Press Enter to continue...")


# ___________________________________________Profile Management____________________________________________________________

def profile_flow(user):
    while True:
        print_menu(
            [
                "View Profile",
                "Change Username",
                "Change Phone",
                "Change Password",
                "Back"
            ],
            title="Profile Management"
        )

        choice = get_choice(5)

        if choice == 1:
            profile = get_user_profile(user.id)

            print_info(
                f"Username: {profile.username}\n"
                f"Birth Date: {profile.birth_date}\n"
                f"Phone: {profile.phone}\n"
                f"Wallet Balance: ${profile.wallet_balance:.2f}"
            )
            input("Press Enter to continue...")

        elif choice == 2:
            new_username = get_input("New Username: ")

            try:
                change_username(user.id, new_username)
                user.username = new_username

                logger.info(f"Username changed for user_id: {user.id} to {new_username}")

                print_success("Username updated successfully!")
                input("Press Enter to continue...")

            except CinemaTicketError as e:
                logger.exception(f"Error changing username: {e}")
                print_error(str(e))
                input("Press Enter to continue...")

        elif choice == 3:
            new_phone = get_input("New Phone (leave blank to remove): ", required=False)
            new_phone = new_phone or None

            try:
                change_phone(user.id, new_phone)
                user.phone = new_phone

                logger.info(f"Phone changed for user_id: {user.id} to {new_phone}")

                print_success("Phone number updated successfully!")
                input("Press Enter to continue...")

            except CinemaTicketError as e:
                logger.exception(f"Error changing phone: {e}")
                print_error(str(e))
                input("Press Enter to continue...")

        elif choice == 4:
            current_password = getpass("Current Password: ")
            new_password = getpass("New Password: ")
            confirm_password = getpass("Confirm Password: ")

            try:
                change_password(user.id, current_password, new_password, confirm_password)

                logger.info(f"Password changed for user_id: {user.id}")

                print_success("Password updated successfully!")
                input("Press Enter to continue...")

            except CinemaTicketError as e:
                logger.exception(f"Error changing password: {e}")
                print_error(str(e))
                input("Press Enter to continue...")

        else:
            break