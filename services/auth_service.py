"""
Authentication service.

Responsibilities:
- Register user
- Login user

Uses:
- ID as primary key
- username_index for O(1) lookup
"""


from core.user import User
from storage.json_storage import load_users, save_users
from utils.exceptions import (
    UsernameAlreadyExistsError,
    InvalidCredentialsError,
    UserNotFoundError,
)
from utils.logger import get_logger

logger = get_logger(__name__)

def register_user(
        username: str,
        password: str,
        birth_date: str,
        phone: str|None=None
    ) -> User:
    """
    Registers a new user.

    Steps:
    1. Load users
    2. Check username uniqueness (O(1))
    3. Create User object
    4. Save in:
        - by_id
        - username_index
    """

    data = load_users()
    users_by_id = data["by_id"]
    username_index = data["username_index"]

    username = username.strip()

    if username in username_index:
        logger.warning(f"Registration failed: username '{username}' exists")
        raise UsernameAlreadyExistsError(username)

           

    try:
        user = User(
            username=username,
            password=password,
            birth_date=birth_date,
            phone=phone,
        )
    except Exception as e:
        logger.error(f"User creation failed for '{username}': {e}")
        raise

    try:
        users_by_id[user.id] = user.to_dict()
        username_index[username] = user.id

        save_users(data)

        logger.info(f"User registered: {username}")

    except Exception as e:
        logger.error(f"Failed to save user '{username}': {e}")
        raise

    return user   


def login_user(username: str, password: str) -> User:
    """
    Login flow:

    1. Load users
    2. Find user_id using username_index (O(1))
    3. Load user data by ID
    4. Check password
    """
    data = load_users()
    users_by_id = data["by_id"]
    username_index = data["username_index"]

    username = username.strip()

    if username not in username_index:
        logger.warning(f"Login failed: username '{username}' not found")
        raise UserNotFoundError(username)
    
    user_id = username_index[username]
    user_data = users_by_id.get(user_id)

    if not user_data:
        # Data inconsistency protection
        logger.error(f"User ID '{user_id}' missing for username '{username}'")
        raise InvalidCredentialsError()
    
    try:
        user = User.from_dict(user_data)
    except Exception as e:
        logger.error(f"Failed to load user '{username}': {e}")
        raise InvalidCredentialsError()
    
    if not user.check_password(password):
        logger.warning(f"Login failed: wrong password for '{username}'")
        raise InvalidCredentialsError()
    
    logger.info(f"User logged in successfully: {username} (id={user.id})")
    return user