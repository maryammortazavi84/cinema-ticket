"""
Subscription Service
This module provides functions to manage user subscriptions, including creating new subscriptions, retrieving existing subscriptions, and
applying subscription benefits to user transactions. It interacts with the Subscription domain model and handles persistence through the JSON storage layer.
Key functionalities include:
- get_user_subscription: Retrieve a user's subscription details.
- create_subscription: Create a new subscription for a user.
- has_active_subscription: Check if a user has an active subscription.
- get_user_subscription_type: Get the subscription type of a user, defaulting to bronze if no active subscription exists.
- apply_subscription_benefits: Apply subscription benefits to a given amount based on the user's active subscription.
- remaining_gold_drink_benefits: Check if the user has remaining drink benefits from a
gold subscription and apply one if available.
"""
from decimal import Decimal
from core.subscription import Subscription
from core.enums import SubscriptionType
from core.user import User
from storage.json_storage import load_subscriptions, save_subscriptions
from datetime import datetime, timedelta
from utils.exceptions import (
    InvalidSubscriptionTypeError,
)
from utils.logger import get_logger
logger = get_logger(__name__)

# ============== helper functions (private to this service) ==============
def _load_user_subscriptions(user_id:str) -> Subscription | None:
    """
    Load a user's subscription from storage.
    Args:
        user_id: Unique identifier of the user.
    Returns:
        Subscription: Deserialized Subscription object if exists, else None.
    """
    data = load_subscriptions()
    if user_id not in data["by_user_id"]:
        logger.warning(f"No subscription found for user_id: {user_id}")
        return None

    try:
        return Subscription.from_dict(data["by_user_id"][user_id])     
    except Exception as e:
        logger.error(f"Failed to load/deserialize subscription for user_id {user_id}: {e}", exc_info=True)
        raise

def _save_user_subscription(subscription: Subscription) -> None:
    """
    Persist a user's subscription to storage.
    Args:
        subscription: Subscription instance to be saved.
    """
    data = load_subscriptions()
    data["by_user_id"][subscription.user_id] = subscription.to_dict()
    save_subscriptions(data)

    logger.info(f"Subscription for user_id {subscription.user_id} saved successfully")


# ====================================================

def get_user_subscription(user_id: str) -> Subscription | None:
    """
    Retrieve a user's subscription details.
    Args:
        user_id: Unique identifier of the user.
    Returns:
        Subscription: User's subscription if exists, else None.
    """
    sub =  _load_user_subscriptions(user_id)
    if sub is None:
        logger.info(f"User {user_id} does not have an active subscription.")
        return None
    
    if not sub.is_active():
        logger.info(f"User {user_id} has an expired subscription.")
        return None
    
    logger.info(f"User {user_id} has an active subscription: {sub}")
    return sub



def create_subscription(user_id: str, subscription_type: SubscriptionType) -> Subscription:
    """
    Create a new subscription for a user.
    Args:   
        user_id: Unique identifier of the user.
        subscription_type: Type of subscription to create (e.g., BASIC, GOLD).  
    Returns:
        Subscription: The newly created subscription object.
    Raises:
        InvalidSubscriptionTypeError: If the provided subscription type is not valid.
    """
    if not isinstance(subscription_type, SubscriptionType):
        logger.error(f"Invalid subscription type: {subscription_type}")
        raise InvalidSubscriptionTypeError(subscription_type)
    
    start_date = datetime.datetime.now(datetime.timezone.utc)

    if subscription_type == SubscriptionType.GOLD:
        end_date = start_date + timedelta(days=30)
    else:
        end_date = None  # No end date for basic subscription

    subscription = Subscription(
        user_id=user_id,
        subscription_type=subscription_type,
        start_date=start_date.strftime("%Y-%m-%d"),
        end_date=end_date.strftime("%Y-%m-%d") if end_date else None
    )

    _save_user_subscription(subscription)
    logger.info(f"Created new subscription for user_id {user_id}: {subscription}")

    return subscription
        

def has_active_subscription(user_id: str) -> bool:
    sub = get_user_subscription(user_id)

    if sub is None:
        logger.info(f"User {user_id} does not have an active subscription.")
        return False

    logger.info(f"User {user_id} has an active subscription.")
    return True


def get_user_subscription_type(user_id: str) -> SubscriptionType :
    """
    Get the subscription type of a user. If the user does not have an active subscription, returns SubscriptionType.BRONZE.
    Args:
    user_id: Unique identifier of the user.
    Returns:    
    SubscriptionType: The subscription type of the user, or SubscriptionType.BRONZE if no active subscription exists.

    """
    sub = get_user_subscription(user_id)

    if sub is None:
        logger.info(f"User {user_id} does not have an active subscription. Defaulting to bronze.")
        return SubscriptionType.BRONZE

    logger.info(f"User {user_id} has an active subscription of type {sub.subscription_type}.")
    return sub.subscription_type
    
   
def apply_subscription_benefits(user: User, amount: Decimal) -> Decimal:
    """
    Apply subscription benefits to a given amount based on the user's active subscription.
    Args:
    user: User instance for whom to apply benefits.
    amount: Original amount before applying benefits.   
    Returns:
    Decimal: Final amount after applying subscription benefits.

    """
    sub = get_user_subscription(user.id)

    if sub is None:
        logger.info(f"User {user.id} has bronze subscription. No benefits applied.")
        return amount
    
    
    sub_type = sub.subscription_type
    if sub_type == SubscriptionType.SILVER:
        if sub.remaining_credits <= 0:
            logger.info(f"User {user.id} has silver subscription but no remaining credits. No benefits applied.")
            return amount
            
        cashback = amount * Decimal("0.2")
        final_amount = amount - cashback
        user.deposit(cashback)
        logger.info(f"Applied silver subscription benefits for user {user.id}: original amount {amount}, cashback {cashback}, final amount {final_amount}")
        sub.remaining_credits -= 1
        _save_user_subscription(sub)
        return amount
    elif sub_type == SubscriptionType.GOLD:
            
        discount = amount * Decimal("0.5")
        final_amount = amount - discount
        logger.info(f"Applied gold subscription benefits for user {user.id}: original amount {amount}, discount {discount}, final amount {final_amount}")
        return final_amount
    else:
        logger.warning(f"Unknown subscription type {sub_type} for user {user.id}. No benefits applied.")
        return amount
    

def remaining_gold_drink_benefits(user: User) -> bool:
    """
    Check if the user has remaining drink benefits from a gold subscription and apply one if available.
    Args:
    user: User instance to check for gold drink benefits.
    Returns:
    bool: True if a drink benefit was applied, False otherwise.
    """
    sub = get_user_subscription(user.id)

    if sub is None or sub.subscription_type != SubscriptionType.GOLD:
        logger.info(f"User {user.id} does not have an active gold subscription. No drink benefits applied.")
        return False
    
    if sub.apply_gold_drink_benefits <= 0:
        logger.info(f"User {user.id} has gold subscription but has already used the drink benefit. No benefits applied.")
        return False

    sub.apply_gold_drink_benefits -= 1
    _save_user_subscription(sub)
    logger.info(f"Applied gold drink benefit for user {user.id}. Remaining drink benefits: {sub.apply_gold_drink_benefits}")
    return True