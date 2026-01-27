"""
Security utilities for the Cinema Ticket project.

Provides functions for:
- Password hashing and verification (using hashlib)
- Generating unique IDs (using uuid)
- Securely reading passwords from input (using getpass)
"""

import hashlib
import uuid
import hmac
from getpass import getpass
from typing import Tuple

def hash_password(password: str) -> Tuple[str, str]:
    """Hashes a password using PBKDF2 with HMAC-SHA256."""
    salt = uuid.uuid4().bytes

    hashed = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    return salt.hex(), hashed.hex()


def verify_password(stored_salt_hex:str, stored_hash_hex:str, provided_password:str) -> bool:
    """Verifies a password against a stored salt and hash."""
    salt = bytes.fromhex(stored_salt_hex)
    stored_hash = bytes.fromhex(stored_hash_hex)

    computed_hash = hashlib.pbkdf2_hmac('sha256', provided_password.encode(), salt, 100000)

    return hmac.compare_digest(computed_hash, stored_hash)


def generate_unique_id() -> str:
    """Generates a unique identifier using UUID4."""
    return uuid.uuid4().hex


def secure_input(prompt: str = "Password: ") -> str:
    """Securely reads input from user without echoing (ideal for passwords)."""

    return getpass(prompt= prompt)



