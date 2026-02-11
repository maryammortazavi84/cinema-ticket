"""
User service for Cinema Ticket project.

Provides operations for managing authenticated user data, including:
- Updating profile information (username, phone number)
- Changing password with current password verification

This module handles business logic and persistence for user updates.
"""

from core.user import User
from storage.json_storage import load_users, save_users
from utils.exceptions import (
    UserNotFoundError,
    UsernameAlreadyExistsError,
    WrongPasswordError,
    PasswordMismatchError
    )
from utils.logger import get_logger
logger = get_logger(__name__)

# ────────────────────────────────────────────────
# Helper functions (private to this service)
# ────────────────────────────────────────────────

def _load_user_by_id(user_id: str) -> User:
    """
    Load a user from storage by their unique ID.

    Args:
        user_id: Unique identifier of the user.

    Returns:
        User: Deserialized User object.

    Raises:
        UserNotFoundError: If the user does not exist in storage.
        Exception: If deserialization fails.
    """
    data = load_users()
    if user_id not in data["by_id"]:
        logger.error(f"User not found for id: {user_id}")
        raise UserNotFoundError()

    try:
        return User.from_dict(data["by_id"][user_id])
    except Exception as e:
        logger.error(f"Failed to load/deserialize user {user_id}: {e}", exc_info=True)
        raise



def _save_user(user: User, *, update_index: bool = False, old_username: str | None = None) -> None:
    """
    Persist user changes to storage.

    Optionally updates the username index if the username has changed.

    Args:
        user: User instance to be saved.
        update_index: Whether the username index should be updated.
        old_username: Previous username (required if update_index is True).
    """

    data = load_users()
    data["by_id"][user.id] = user.to_dict()

    if update_index and old_username:
        username_index = data["username_index"]
        if old_username in username_index:
            del username_index[old_username]
        username_index[user.username] = user.id

    save_users(data)
    logger.debug(f"User saved/updated: {user.id} ({user.username})")



def change_phone(user_id: str, new_phone: str) -> User:
    """
    Update the phone number of a user.

    Args:
        user_id: Unique identifier of the user.
        new_phone: New phone number.

    Returns:
        User: Updated user instance.

    Raises:
        UserNotFoundError: If the user does not exist.
        Exception: If phone validation or update fails.
    """

    user = _load_user_by_id(user_id)
        
    try:    
        user.phone = new_phone
    except Exception as e:
        logger.error(f"Change phone failed for user '{user_id}': {e}")
        raise
    
    _save_user(user)
    logger.info(f"Phone updated for user {user.username} (id: {user_id})")

    return user


    
def change_username(user_id: str, new_username: str) -> User:
    """
    Change a user's username if the new username is available.

    If the new username is the same as the current one, no changes are made.

    Args:
        user_id: Unique identifier of the user.
        new_username: Desired username.

    Returns:
        User: Updated user instance.

    Raises:
        UserNotFoundError: If the user does not exist.
        UsernameAlreadyExistsError: If the username is already taken by another user.
    """

    data = load_users()
    username_index = data["username_index"]

    
    
    if new_username in username_index and username_index[new_username] != user_id:
        raise UsernameAlreadyExistsError(new_username)
    
    user = _load_user_by_id(user_id)

    if user.username == new_username:
        logger.info(f"Username already is '{new_username}', no change needed")
        return user
    
    old_username = user.username
    user.username = new_username

    if old_username in username_index:
        del username_index[old_username]
    username_index[new_username] = user_id

    _save_user(user, update_index=True, old_username=old_username)
    logger.info(f"Username changed: '{old_username}' → '{new_username}'")
    return user

    
def change_password(
        user_id: str, 
        current_password: str, 
        new_password: str, 
        confirm_password: str) -> User:
    """
    Change a user's password after verifying the current password.

    The new password must match the confirmation and must be different
    from the current password.

    Args:
        user_id: Unique identifier of the user.
        current_password: User's current password.
        new_password: New password.
        confirm_password: Confirmation of the new password.

    Returns:
        User: Updated user instance.

    Raises:
        UserNotFoundError: If the user does not exist.
        WrongPasswordError: If the current password is incorrect.
        PasswordMismatchError: If new password and confirmation do not match.
        Exception: If password update fails.
    """

    user = _load_user_by_id(user_id)

    if not user.check_password(current_password):
        logger.warning(f"Failed to change password for user_id '{user_id}'.Wrong password")
        raise WrongPasswordError()
    
    if new_password != confirm_password:
        logger.error(f"Failed to change password for user_id '{user_id}'.New password and confirmation do not match.")
        raise PasswordMismatchError()
    
    if new_password == current_password:
        logger.info(f"Password unchanged for user {user_id}")
        return user
    
    
    try:
        user.set_password(new_password)
    except Exception as e:
        logger.error(f"Failed to change password for user_id '{user_id}': {e}")
        raise

    
    _save_user(user)
    logger.info(f"Password successfully changed for user {user_id}")
    return user


def get_user_profile(user_id: str) -> User:
    """
    Retrieve a user's profile information.

    Args:
        user_id: Unique identifier of the user.

    Returns:
        User: User instance containing profile information.

    Raises:
        UserNotFoundError: If the user does not exist.
        Exception: If loading the user fails.
    """
    try:
        user = _load_user_by_id(user_id)
        logger.info(f"User profile retrieved for user_id '{user_id}'")
        return user
    except Exception as e:
        logger.error(f"Failed to retrieve user profile for user_id '{user_id}': {e}")
        raise



    








