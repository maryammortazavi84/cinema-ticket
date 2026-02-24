import pytest
from datetime import datetime, timedelta

from core.subscription import Subscription
from core.enums import SubscriptionType
from utils.exceptions import InvalidSubscriptionTypeError, InvalidDateError


# -----------------------------
# Helpers
# -----------------------------
def today_str():
    return datetime.today().strftime("%Y-%m-%d")


def future_str(days=10):
    return (datetime.today() + timedelta(days=days)).strftime("%Y-%m-%d")


def past_str(days=10):
    return (datetime.today() - timedelta(days=days)).strftime("%Y-%m-%d")


# -----------------------------
# Creation Tests
# -----------------------------
def test_create_silver_subscription_success():
    sub = Subscription(
        user_id="u1",
        subscription_type=SubscriptionType.SILVER,
        start_date=today_str(),
        end_date=future_str()
    )

    assert sub.user_id == "u1"
    assert sub.subscription_type == SubscriptionType.SILVER
    assert sub.remaining_credits == 3


def test_create_gold_subscription_drink_flag():
    sub = Subscription(
        user_id="u1",
        subscription_type=SubscriptionType.GOLD,
        start_date=today_str(),
        end_date=future_str()
    )

    assert sub.apply_gold_drink_benefits == 1
    assert sub.remaining_credits == 0


# -----------------------------
# Validation Tests
# -----------------------------
def test_invalid_subscription_type_raises():
    with pytest.raises(InvalidSubscriptionTypeError):
        Subscription(
            user_id="u1",
            subscription_type="gold",  # wrong type
            start_date=today_str(),
            end_date=future_str()
        )


def test_invalid_date_format_raises():
    with pytest.raises(InvalidDateError):
        Subscription(
            user_id="u1",
            subscription_type=SubscriptionType.GOLD,
            start_date="2025/99/99",
            end_date="2025/99/99"
        )


def test_end_before_start_raises():
    with pytest.raises(InvalidDateError):
        Subscription(
            user_id="u1",
            subscription_type=SubscriptionType.GOLD,
            start_date=today_str(),
            end_date=past_str()
        )


# -----------------------------
# is_active Tests
# -----------------------------
def test_gold_is_active_true():
    sub = Subscription(
        user_id="u1",
        subscription_type=SubscriptionType.GOLD,
        start_date=today_str(),
        end_date=future_str()
    )

    assert sub.is_active() is True


def test_gold_is_active_false_when_expired():
    sub = Subscription(
        user_id="u1",
        subscription_type=SubscriptionType.GOLD,
        start_date=past_str(20),
        end_date=past_str(10)
    )

    assert sub.is_active() is False


def test_silver_is_active_based_on_credits():
    sub = Subscription(
        user_id="u1",
        subscription_type=SubscriptionType.SILVER,
        start_date=today_str(),
        end_date=future_str()
    )

    assert sub.is_active() is True

    sub.remaining_credits = 0
    assert sub.is_active() is False


def test_bronze_is_not_active():
    sub = Subscription(
        user_id="u1",
        subscription_type=SubscriptionType.BRONZE,
        start_date=today_str(),
        end_date=future_str()
    )

    assert sub.is_active() is False


# -----------------------------
# Serialization Tests
# -----------------------------
def test_to_dict_and_from_dict():
    sub = Subscription(
        user_id="u1",
        subscription_type=SubscriptionType.SILVER,
        start_date=today_str(),
        end_date=future_str()
    )

    data = sub.to_dict()
    new_sub = Subscription.from_dict(data)

    assert new_sub.user_id == sub.user_id
    assert new_sub.subscription_type == sub.subscription_type
    assert new_sub.remaining_credits == sub.remaining_credits