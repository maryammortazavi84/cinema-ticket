from __future__ import annotations
from datetime import datetime, date
from utils.security import hash_password, verify_password, generate_unique_id
from utils.exceptions import (InvalidPasswordError,
                            InsufficientBalanceError,
                            InvalidAmountError,
                            InvalidUserNameError,
                            InvalidPhoneNumberError,
                            InvalidBirthDateError)
from decimal import Decimal
import re

class User:
    """
    Domain model representing a system user.

    Handles user data, password security, wallet balance (with Decimal precision),
    and basic validation for username, phone, and birth date.

    Attributes are protected via properties and setters for encapsulation and validation.
    """

    # CONSTRUCTOR 
    def __init__(self, 
                username: str, 
                password: str, 
                birth_date: str,
                phone: str | None = None,
                *,
                user_id: str | None = None,
                salt: str | None = None,
                password_hash: str | None = None,
                wallet_balance: Decimal = Decimal("0.0"),
                created_at: str | None = None
                ):
        """
        Initialize a new user or load from stored data.

        Args:
            username: Unique username (min 3 chars)
            password: Plain password (required for new users)
            birth_date: Birth date string (multiple formats supported)
            phone: Optional phone number (Iranian format: 09xxxxxxxxx)
            user_id: Optional pre-generated ID (auto-generated if None)
            salt/password_hash: For loading existing user
            wallet_balance: Initial balance (non-negative Decimal)
            created_at: ISO datetime string (auto-generated if None)

        Raises:
            Various Invalid*Error exceptions for validation failures
        """
        
        # immutable/system fields
        self._id: str = user_id or generate_unique_id()
        self._created_at: datetime = (datetime.fromisoformat(created_at) if created_at else datetime.now())

        # validated fields via setters
        self.username = username
        self.birth_date = birth_date
        self.phone = phone

        # wallet
        self._wallet_balance: Decimal = Decimal("0.0")
        self._set_initial_balance(wallet_balance)
        
        # security
        if salt and password_hash:
            self._salt = salt
            self._password_hash = password_hash
        else:
            self.set_password(password)

    # READ-ONLY PROPERTIES
    
    @property
    def id(self) -> str:
        return self._id
    
    @property
    def created_at(self) -> datetime:
        return self._created_at
    
    @property
    def salt(self) -> str:
        return self._salt
    
    @property
    def password_hash(self) -> str:
        return self._password_hash

    # USERNAME 

    @property
    def username(self) -> str:
        return self._username
    
    @username.setter
    def username(self, value: str) -> None:
        value = value.strip()
        if not value or len(value) < 3:
            raise InvalidUserNameError(value)
        self._username = value
        
    def __repr__(self):
        return f'User(id={self.id}, username={self.username})'

    # PHONE 

    @property
    def phone(self):
        return self._phone
    
    @phone.setter
    def phone(self, value: str | None):
        if value is None or value.strip() == "":
            self._phone = None
            return
        
        if not re.fullmatch(r"09\d{9}", value):
            raise InvalidPhoneNumberError
        
        self._phone = value

    # BIRTH DATE

    @property
    def birth_date(self) -> str:
        return self._birth_date.strftime("%Y-%m-%d")
    
    @birth_date.setter
    def birth_date(self, value: str) -> None:
        valid_formats = ["%Y-%m-%d", "%d/%m/%Y", "%d.%m.%Y"]
        
        for fmt in valid_formats:
            try:
                dt = datetime.strptime(value, fmt).date()
                break
            except ValueError:
                continue
        else:
            raise InvalidBirthDateError(value, "Incorrect format, use YYYY-MM-DD or DD/MM/YYYY or DD.MM.YYYY")
        
        if dt > date.today():
            raise InvalidBirthDateError(value, "Birth date is in the future")
        
        if dt.year < 1900:
            raise InvalidBirthDateError(value, "Birth date is unrealistically old")
        
        self._birth_date: date = dt

    # AGE 
    @property
    def age(self) -> int:                     
        today = date.today()
        birth = self._birth_date
        return today.year - birth.year - (
            (today.month, today.day) < (birth.month, birth.day)
        )

    # WALLET 

    @property
    def wallet_balance(self) -> Decimal:
        return self._wallet_balance

    def _set_initial_balance(self, value: Decimal) -> None:
        value = Decimal(str(value))  # ⭐
        if value < 0:
            raise InvalidAmountError(value)
        self._wallet_balance = value

    def deposit(self, amount: Decimal) -> None:
        amount = Decimal(str(amount))  # ⭐
        if amount <= 0:
            raise InvalidAmountError(amount)
        self._wallet_balance += amount

    def withdraw(self, amount: Decimal) -> None:
        amount = Decimal(str(amount))  # ⭐
        if amount <= 0:
            raise InvalidAmountError(amount)
        if amount > self._wallet_balance:
            raise InsufficientBalanceError(amount, self._wallet_balance)
        self._wallet_balance -= amount
       
    # PASSWORD 

    def set_password(self, password: str) -> None:
        if len(password) < 8:
            raise InvalidPasswordError("Password must be at least 8 characters.")
        
        if not any(c.isupper() for c in password):
            raise InvalidPasswordError("Password must contain an uppercase letter.")
        
        if not any(c.islower() for c in password):
            raise InvalidPasswordError("Password must contain a lowercase letter.")
        
        if not any(c.isdigit() for c in password):
            raise InvalidPasswordError("Password must contain a number.")
        
        self._salt, self._password_hash = hash_password(password)


    def check_password(self, password: str) -> bool:
        return verify_password(self.salt, self.password_hash, password)

    # SERIALIZATION 

    def to_dict(self) -> dict:
        return {
            "id" : self.id,
            "username" : self.username,
            "phone" : self.phone,
            "birth_date" : self.birth_date,
            "salt" : self.salt,
            "password_hash" : self.password_hash,
            "wallet_balance" : self.wallet_balance,
            "created_at" : self._created_at.isoformat(),
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "User":
        return cls(
            username=data["username"],
            password="", # not used when salt/hash exist 
            birth_date=data["birth_date"],
            phone=data.get("phone"),
            user_id=data["id"],
            salt=data["salt"],
            password_hash=data["password_hash"],
            wallet_balance=data.get("wallet_balance", 0.0),
            created_at=data.get("created_at"),
        )



        