import pytest
from services.auth_service import register_user, login_user
from utils.exceptions import UsernameAlreadyExistsError, UserNotFoundError, InvalidCredentialsError

# ------------------------------
# Fixtures
# ------------------------------
@pytest.fixture
def fake_storage():
    """Fake in-memory users data structure"""
    return {
        "by_id": {},
        "username_index": {}
    }

# ------------------------------
# Tests for register_user
# ------------------------------
def test_register_user_success(monkeypatch, fake_storage):
    # Mock load_users
    monkeypatch.setattr("services.auth_service.load_users", lambda: fake_storage)
    # Mock save_users
    monkeypatch.setattr("services.auth_service.save_users", lambda data: None)

    user = register_user("mary", "StrongPass123", "2000-01-01", "09123456789")

    assert user.username == "mary"
    assert "mary" in fake_storage["username_index"]
    assert user.id == fake_storage["username_index"]["mary"]
    assert fake_storage["by_id"][user.id]["username"] == "mary"

def test_register_user_duplicate(monkeypatch, fake_storage):
    monkeypatch.setattr("services.auth_service.load_users", lambda: fake_storage)
    monkeypatch.setattr("services.auth_service.save_users", lambda data: None)

    # pre-add a user
    fake_storage["by_id"]["123"] = {"username": "mary", "id": "123"}
    fake_storage["username_index"]["mary"] = "123"

    with pytest.raises(UsernameAlreadyExistsError):
        register_user("mary", "StrongPass123", "2000-01-01")

# ------------------------------
# Tests for login_user
# ------------------------------
def test_login_user_success(monkeypatch, fake_storage):
    # Create user dict manually
    user_dict = {
        "id": "abc123",
        "username": "john",
        "phone": None,
        "birth_date": "2000-01-01",
        "salt": "abcd",
        "password_hash": "1234",
        "wallet_balance": 0.0,
        "created_at": "2026-02-07T00:00:00"
    }

    # Fake check_password always True
    class FakeUser:
        def __init__(self, data):
            self.username = data["username"]
            self.id = data["id"]
        def check_password(self, password):
            return True
        @classmethod
        def from_dict(cls, data):
            return cls(data)

    monkeypatch.setattr("services.auth_service.load_users", lambda: fake_storage)
    monkeypatch.setattr("services.auth_service.User", FakeUser)

    fake_storage["by_id"]["abc123"] = user_dict
    fake_storage["username_index"]["john"] = "abc123"

    user = login_user("john", "whatever")
    assert user.username == "john"
    assert user.id == "abc123"

def test_login_user_not_found(monkeypatch, fake_storage):
    monkeypatch.setattr("services.auth_service.load_users", lambda: fake_storage)

    with pytest.raises(UserNotFoundError):
        login_user("nobody", "pass")

def test_login_user_wrong_password(monkeypatch, fake_storage):
    # Fake check_password always False
    class FakeUser:
        def __init__(self, data):
            self.username = data["username"]
            self.id = data["id"]
        def check_password(self, password):
            return False
        @classmethod
        def from_dict(cls, data):
            return cls(data)

    monkeypatch.setattr("services.auth_service.load_users", lambda: fake_storage)
    monkeypatch.setattr("services.auth_service.User", FakeUser)

    fake_storage["by_id"]["abc123"] = {"username": "john", "id": "abc123"}
    fake_storage["username_index"]["john"] = "abc123"

    with pytest.raises(InvalidCredentialsError):
        login_user("john", "wrongpass")
