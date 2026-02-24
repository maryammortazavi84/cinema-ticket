# tests/test_subscription_service.py

import pytest
from decimal import Decimal
from datetime import datetime, timedelta

from core.enums import SubscriptionType
from core.user import User
from services.subscription_service import (
    create_subscription,
    get_user_subscription,
    has_active_subscription,
    apply_subscription_benefits,
    remaining_gold_drink_benefits,
)
from storage.json_storage import save_subscriptions


# ---------- helpers ----------

def reset_storage():
    save_subscriptions({"by_user_id": {}})


def create_test_user(user_id: str = "user_1") -> User:
    return User(
        username="testuser",
        password="Test123!",
        birth_date="2000-01-01",
        phone="09123456789",
        user_id=user_id,
    )


# ---------- tests ----------

def setup_function():
    reset_storage()


def test_create_and_get_subscription():
    user_id = "user_1"

    create_subscription(user_id, SubscriptionType.GOLD)
    sub = get_user_subscription(user_id)

    assert sub is not None
    assert sub.subscription_type == SubscriptionType.GOLD


def test_has_active_subscription_true():
    user_id = "user_2"

    create_subscription(user_id, SubscriptionType.GOLD)

    assert has_active_subscription(user_id) is True


def test_has_active_subscription_false():
    user_id = "user_3"

    assert has_active_subscription(user_id) is False


def test_silver_cashback_applied():
    user = create_test_user("user_4")

    # create silver subscription manually
    create_subscription(user.id, SubscriptionType.SILVER)

    original_balance = user.wallet_balance

    amount = Decimal("100")
    final_amount = apply_subscription_benefits(user, amount)

    # silver gives 20% cashback to wallet
    assert final_amount == amount
    assert user.wallet_balance == original_balance + Decimal("20")


def test_gold_discount_applied():
    user = create_test_user("user_5")

    create_subscription(user.id, SubscriptionType.GOLD)

    amount = Decimal("100")
    final_amount = apply_subscription_benefits(user, amount)

    assert final_amount == Decimal("50")


def test_gold_drink_benefit_once():
    user = create_test_user("user_6")

    create_subscription(user.id, SubscriptionType.GOLD)

    first = remaining_gold_drink_benefits(user)
    second = remaining_gold_drink_benefits(user)

    assert first is True
    assert second is False