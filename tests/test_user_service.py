# tests/test_user_service.py
import pytest
from core.user import User
from core.enums import UserRole
from services import user_service
from utils.exceptions import (
    UserNotFoundError,
    UsernameAlreadyExistsError,
    WrongPasswordError,
    PasswordMismatchError
)
from storage.json_storage import save_users

# ───── Fixture ─────
@pytest.fixture
def sample_user():
    user = User(
        username="maryam",
        password="StrongPass123",
        birth_date="1995-05-05",
        phone="09123456789",
        user_id="fixed-user-id"
    )

    user.set_password("StrongPass123")

    save_users({
        "by_id": {user.id: user.to_dict()},
        "username_index": {user.username: user.id}
    })
    return user

# ───── Test change_phone ─────
def test_change_phone_success(sample_user):
    updated_user = user_service.change_phone(sample_user.id, "09998887766")
    assert updated_user.phone == "09998887766"

def test_change_phone_user_not_found():
    with pytest.raises(UserNotFoundError):
        user_service.change_phone("non-existent-id", "09998887766")

# ───── Test change_username ─────
def test_change_username_success(sample_user):
    updated_user = user_service.change_username(sample_user.id, "newusername")
    assert updated_user.username == "newusername"

def test_change_username_duplicate(sample_user):

    duplicate_user = User(
        username="duplicate",
        password="StrongPass123",
        birth_date="1990-01-01",
        user_id="other-id"
    )
    duplicate_user.set_password("StrongPass123")
    save_users({
        "by_id": {sample_user.id: sample_user.to_dict(),
                  duplicate_user.id: duplicate_user.to_dict()},
        "username_index": {sample_user.username: sample_user.id,
                           duplicate_user.username: duplicate_user.id}
    })

    with pytest.raises(UsernameAlreadyExistsError):
        user_service.change_username(sample_user.id, "duplicate")

# ───── Test change_password ─────
def test_change_password_success(sample_user):
    updated_user = user_service.change_password(
        sample_user.id, 
        current_password="StrongPass123",
        new_password="NewStrongPass456",
        confirm_password="NewStrongPass456"
    )
    assert updated_user.check_password("NewStrongPass456")

def test_change_password_wrong_current(sample_user):
    with pytest.raises(WrongPasswordError):
        user_service.change_password(
            sample_user.id,
            current_password="WrongPass",
            new_password="NewPass123",
            confirm_password="NewPass123"
        )

def test_change_password_mismatch(sample_user):
    with pytest.raises(PasswordMismatchError):
        user_service.change_password(
            sample_user.id,
            current_password="StrongPass123",
            new_password="NewPass123",
            confirm_password="DifferentPass123"
        )

# ───── Test get_user_profile ─────
def test_get_user_profile_success(sample_user):
    user = user_service.get_user_profile(sample_user.id)
    assert user.username == "maryam"

def test_get_user_profile_not_found():
    with pytest.raises(UserNotFoundError):
        user_service.get_user_profile("non-existent-id")
