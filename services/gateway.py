"""
Gateway service for processing payments.
"""
from utils.logger import get_logger
from decimal import Decimal
from utils.exceptions import InvalidAmountError

logger = get_logger(__name__)

class Gateway:
    """
    Gateway service for processing payments."""

    def __init__(self, gateway_id: str):
        """
        Initialize the Gateway service.
        """
        self.gateway_id = gateway_id
        logger.info(f"Gateway service initialized with ID: {gateway_id}")

        self.transactions = []  # List to store transaction records

    def process_amount(self, amount: Decimal, user_id: str, discription: str) -> bool:
        """
        Process a payment amount for a given user.

        Args:
            amount: The amount to process.
            user_id: The ID of the user making the payment.
        """

        if amount <= 0:
            logger.error(f"Invalid amount: {amount} for user_id: {user_id}")
            raise InvalidAmountError(amount)

        
        logger.info(f"Processing amount: {amount} for user_id: {user_id} with description: {discription}")
        self.transactions.append({
            "user_id": user_id,
            "amount": amount,
            "description": discription
        })

        logger.info(f"Payment of {amount} for user_id: {user_id} processed successfully.")
        return True




