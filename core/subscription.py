"""
Module: subscription.py
Description: Defines the Subscription domain model for managing user subscriptions in the cinema ticketing system.
This module includes the Subscription class, which encapsulates subscription details such as type, start and end dates, and remaining credits for silver subscriptions.
The class uses properties and setters to ensure data validation and encapsulation, and it includes methods for checking subscription status and representing the subscription as a string.
"""

from core.enums import SubscriptionType
from datetime import datetime   
from utils.exceptions import InvalidSubscriptionTypeError, InvalidDateError

class Subscription:
    """
    Domain model representing a user's subscription.

    Handles subscription type, start and end dates, and basic validation.

    Attributes are protected via properties and setters for encapsulation and validation.
    """

    def __init__(self, 
                user_id: str,
                subscription_type: SubscriptionType,
                start_date: str,
                end_date: str,
                ):
        """
        Initialize a new subscription.
        Args:
            user_id: ID of the user owning the subscription
            subscription_type: Type of subscription (bronze, silver, gold)
            start_date: Subscription start date (multiple formats supported)
            end_date: Subscription end date (multiple formats supported)
        Raises:
            InvalidSubscriptionTypeError: If subscription type is invalid
            InvalidDateError: If start or end date is invalid
        """

        self._user_id: str = user_id
        self.subscription_type = subscription_type
        self.start_date = start_date
        self.end_date = end_date
        if datetime.strptime(self.end_date, "%Y-%m-%d") < datetime.strptime(self.start_date, "%Y-%m-%d"):
            raise InvalidDateError(end_date, "end_date cannot be before start_date")
        self.remaining_credits = 3 if subscription_type == SubscriptionType.SILVER else 0
        self.apply_gold_drink_benefits = 1 if subscription_type == SubscriptionType.GOLD else 0

    
    # READ-ONLY PROPERTIES
    @property
    def user_id(self) -> str:
        return self._user_id
    
    # SUBSCRIPTION TYPE
    @property
    def subscription_type(self) -> SubscriptionType:
        return self._subscription_type
    
    @subscription_type.setter
    def subscription_type(self, value: SubscriptionType):
        if not isinstance(value, SubscriptionType):
            raise InvalidSubscriptionTypeError(value)
        self._subscription_type = value

    # START DATE
    @property
    def start_date(self) -> str:
        return self._start_date
    
    @start_date.setter
    def start_date(self, value: str):
        valid_formats = ["%Y-%m-%d", "%d/%m/%Y", "%d.%m.%Y"]
        for fmt in valid_formats:
            try:
                parsed_date = datetime.strptime(value, fmt)
                self._start_date = parsed_date.strftime("%Y-%m-%d")
                return
            except ValueError:
                continue
        raise InvalidDateError(value, "Date format is not recognized.")
    
    # END DATE
    @property
    def end_date(self) -> str:
        return self._end_date
    
    @end_date.setter
    def end_date(self, value: str):
        valid_formats = ["%Y-%m-%d", "%d/%m/%Y", "%d.%m.%Y"]
        for fmt in valid_formats:
            try:
                parsed_date = datetime.strptime(value, fmt)
                self._end_date = parsed_date.strftime("%Y-%m-%d")
                return
            except ValueError:
                continue
        raise InvalidDateError(value, "Date format is not recognized.")
    
    def __repr__(self):
        return f"Subscription(user_id={self.user_id}, subscription_type={self.subscription_type}, start_date={self.start_date}, end_date={self.end_date})"
    
    
    def is_active(self) -> bool:
        """Check if the subscription is currently active."""
        if self.subscription_type == SubscriptionType.GOLD:
            if not self.end_date:
                return False
            else:
                today = datetime.today().date()
                start = datetime.strptime(self.start_date, "%Y-%m-%d").date()
                end = datetime.strptime(self.end_date, "%Y-%m-%d").date()
                return start <= today <= end
        elif self.subscription_type == SubscriptionType.SILVER:
            return self.remaining_credits > 0
        else:
            return  False
        
    
    # SERIALIZATION 
    def to_dict(self) -> dict:
        """Convert the subscription object to a dictionary for serialization."""
        return {
            "user_id": self.user_id,
            "subscription_type": self.subscription_type.value,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "remaining_credits": self.remaining_credits
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create a Subscription object from a dictionary."""
        subscription = cls(
        user_id=data["user_id"],
        subscription_type=SubscriptionType(data["subscription_type"]),
        start_date=data["start_date"],
        end_date=data["end_date"]
    )
        subscription.remaining_credits = data.get("remaining_credits", subscription.remaining_credits)
        return subscription
    
    def __str__(self):
        return f"Subscription for user {self.user_id}: {self.subscription_type.value.capitalize()} (Active: {self.is_active()})"
    



