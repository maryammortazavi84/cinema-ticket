from enum import Enum

class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"

class SubscriptionType(str, Enum):
    BRONZE = "bronze"
    SILVER = "silver"
    GOLD = "gold"