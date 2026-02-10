"""
utils.exceptions custom exceptions for project
"""

class CinemaTicketError(Exception):
    """Base exception for all project-related errors."""
    pass


class UsernameAlreadyExistsError(CinemaTicketError):
    """Raised when a user tries to register with an existing username."""
    def __init__(self, username:str, *args):
        self.username = username
        message = f"Username '{username}' already exists."
        super().__init__(message, *args)

class InvalidPasswordError(CinemaTicketError):
    """Raised when password does not meet the minimum requirements."""
    def __init__(self, message: str = "Invalid password format.", *args):
        super().__init__(message, *args)

class WrongPasswordError(CinemaTicketError):
    """Raised when the old password is incorrect during password change."""
    def __init__(self, *args):
        message = "The current password you entered is incorrect."
        super().__init__(message, *args)

class PasswordMismatchError(CinemaTicketError):
    """Raised when new password and confirmation do not match."""
    def __init__(self, *args):
        message = "The new password and its confirmation do not match. Please try again."
        super().__init__(message, *args)

class InvalidUserNameError(CinemaTicketError):
    """raised when user name doesnt match the requierments"""
    def __init__(self, *args):
        message = "Username must be at least 3 characters long"

class UserNotFoundError(CinemaTicketError):
    """Raised when a user with the given username is not found."""
    def __init__(self,  *args):
        message = f"No user found with that user name or id. Please check and try again."
        super().__init__(message, *args)

class InvalidCredentialsError(CinemaTicketError):
    """Raised when username or password is incorrect during login."""
    def __init__(self, *args):
        message = "Invalid username or password. Please check your credentials and try again."
        super().__init__(message, *args)

class InsufficientBalanceError(CinemaTicketError):
    """Raised when wallet balance is not enough for a transaction."""
    def __init__(self, required_amount: float, current_balance: float, *args):
        self.required_amount = required_amount
        self.current_balance = current_balance
        self.shortfall = required_amount - current_balance
        message = (
            f"Insufficient balance. "
            f"Required: {required_amount:.2f} USD, "
            f"Available: {current_balance:.2f} USD. "
            f"You need {self.shortfall:.2f} USD more."
        )
        super().__init__(message, *args)

class InvalidAmountError(CinemaTicketError):
    """Raised when the transaction amount is not positive."""
    def __init__(self, amount: float):
        self.amount = amount
        super().__init__(f"Invalid amount: {amount}. Amount must be positive.")

class SeatAlreadyReservedError(CinemaTicketError):
    """Raised when trying to reserve an already taken seat."""
    def __init__(self, seat_number:str, *args):
        self.seat_number = seat_number
        message = f"The seat {seat_number} is already reserved. Please choose a different seat."
        super().__init__(message, *args)

class ShowtimePassedError(CinemaTicketError):
    """Raised when trying to reserve a showtime that has already passed."""
    def __init__(self, showtime_details: str, *args):
        self.showtime_details = showtime_details
        message = f"The showtime '{showtime_details}' has already passed and cannot be booked."
        super().__init__(message, *args)

class HallFullError(CinemaTicketError):
    def __init__(self, showtime_details:str, capacity:int, *args):
        self.showtime_details = showtime_details
        self.capacity = capacity
        message = (
            f"The hall for the showtime '{showtime_details}' is completely full. "
            f"All {capacity} seats have been reserved. Please choose another showtime."
        )
        super().__init__(message, *args)
    

class AgeRestrictionError(CinemaTicketError):
    """Raised when user's age is below the movie's age rating."""
    def __init__(self, movie_title: str, required_age: int, user_age: int, *args):
        message = (
            f"You are not old enough to watch '{movie_title}'. "
            f"This movie has an age rating of +{required_age}, "
            f"but your age is {user_age}."
        )
        super().__init__(message, *args)
    
    

class InvalidPhoneNumberError(CinemaTicketError):
    """Raised when the provided phone number does not meet the validity requirements."""
    def __init__(self, *args):
        message = (
            f"Please enter a valid phone number (e.g., 09123456789) or leave it blank."
        )
        super().__init__(message, *args)
    

class InvalidBirthDateError(CinemaTicketError):
    """Raised when the provided birth date is invalid or illogical."""
    def __init__(self,birth_date: str, reason: str = "", *args):
        self.birth_date = birth_date
        self.reason = reason
        if reason:
            message = f"The birth date '{birth_date}' is invalid: {reason}."
        else:
            message = f"The birth date '{birth_date}' is invalid. Please enter a valid past date (YYYY-MM-DD)."
        super().__init__(message, *args)
    