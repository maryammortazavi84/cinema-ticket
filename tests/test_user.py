# tests/test_user.py
import pytest
from datetime import date, datetime
from decimal import Decimal


from core.user import User
from utils.exceptions import (
    InvalidPasswordError,
    InvalidUserNameError,
    InvalidPhoneNumberError,
    InvalidBirthDateError,
    InvalidAmountError,
    InsufficientBalanceError,
)


# Fixtures 
@pytest.fixture
def valid_user_data():
    return {
        "username": "maryam",
        "password": "StrongPass123",
        "birth_date": "2005-06-15",
        "phone": "09123456789",
    }



def test_create_user_success(valid_user_data):
    user = User(**valid_user_data)

    assert user.username == "maryam"
    assert user.phone == "09123456789"
    assert user.age > 0  
    assert user.wallet_balance == Decimal("0.0")
    assert isinstance(user.id, str)
    assert isinstance(user.created_at, datetime)
    assert user.check_password("StrongPass123") is True



def test_password_too_short():
    with pytest.raises(InvalidPasswordError, match="at least 8 characters"):
        User(username="test", password="short", birth_date="2000-01-01")



def test_password_no_uppercase():
    with pytest.raises(InvalidPasswordError, match="uppercase letter"):
        User(username="test", password="weakpass123", birth_date="2000-01-01")



def test_username_too_short():
    with pytest.raises(InvalidUserNameError):
        User(username="ab", password="StrongPass123", birth_date="2000-01-01")



def test_invalid_phone():
    with pytest.raises(InvalidPhoneNumberError):
        User(username="test", password="StrongPass123", birth_date="2000-01-01", phone="1234567890")



def test_future_birth_date():
    future_date = (date.today().replace(year=date.today().year + 1)).strftime("%Y-%m-%d")
    with pytest.raises(InvalidBirthDateError, match="in the future"):
        User(username="test", password="StrongPass123", birth_date=future_date)


def test_deposit_and_withdraw():
    user = User(username="test", password="StrongPass123", birth_date="2000-01-01")
    
    user.deposit(Decimal("100.50"))
    assert user.wallet_balance == Decimal("100.50")
    
    user.withdraw(Decimal("40.25"))
    assert user.wallet_balance == Decimal("60.25")



def test_withdraw_insufficient_balance():
    user = User(username="test", password="StrongPass123", birth_date="2000-01-01")
    user.deposit(Decimal("50.0"))
    
    with pytest.raises(InsufficientBalanceError):
        user.withdraw(Decimal("100.0"))



def test_deposit_negative():
    user = User(username="test", password="StrongPass123", birth_date="2000-01-01")
    with pytest.raises(InvalidAmountError):
        user.deposit(Decimal("-10.0"))



def test_from_dict_and_to_dict():
    original = User(username="test", password="StrongPass123", birth_date="2000-01-01")
    data = original.to_dict()
    
    loaded = User.from_dict(data)
    
    assert loaded.id == original.id
    assert loaded.username == original.username
    assert loaded.wallet_balance == original.wallet_balance
    assert loaded.check_password("StrongPass123") is True