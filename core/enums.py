from enum import Enum

class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"

class SubscriptionType(str, Enum):
    BRONZE = "bronze"
    SILVER = "silver"
    GOLD = "gold"

class AgeRating(str, Enum):
    G = 0
    PG = 7
    PG13 = 13
    R = 17
    NC17 = 18

    @property
    def min_age(self) -> int:
        return (self.value)