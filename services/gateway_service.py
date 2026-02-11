"""
Gateway Service Module
This module defines the Gateway_service class, which provides methods for processing payments and managing wallet transactions through
a payment gateway. It serves as an intermediary between the application and the payment gateway, allowing for operations such as depositing to and withdrawing from a user's wallet.
"""

from utils.logger import get_logger
from decimal import Decimal
from gateway import Gateway
from core.user import User

logger = get_logger(__name__)

class Gateway_service:
    """Gateway service for processing payments and managing wallet transactions.
    This service acts as an intermediary between the application and the payment gateway,"""

    def __init__(self, gateway: Gateway):
        """
        Initialize the Gateway service.
        """
        self.gateway = gateway
        logger.info(f"Gateway service initialized with ID: {gateway.gateway_id}")

    def deposit_to_wallet(self, amount: Decimal, user: User, description: str) -> bool:
        """
        Docstring for deposit_to_wallet
        
        Args:            
        amount: The amount to deposit
        user: The User object representing the user making the deposit
        description: Description of the transaction 
        Returns:
            bool: True if the deposit was successful, False otherwise.
        Raises:
            InvalidAmountError: If the amount is invalid.
        """ 
        
        result = self.gateway.process_amount(amount, user.id, description)
        if result:           
            logger.info(f"Deposit of {amount} for user_id: {user.id} .")
        else:
            logger.error(f"Deposit of {amount} for user_id: {user.id} failed.")
        return result
    
    def withdraw_from_wallet(self, amount: Decimal, user: User, description: str) -> bool:
        """
        Withdraw an amount from a user's wallet via the gateway.

        Args:
            amount: The amount to withdraw.
            user: The User object representing the user making the withdrawal.
            description: Description of the transaction.    
        Returns:
            bool: True if the withdrawal was successful, False otherwise.
        Raises:
            InvalidAmountError: If the amount is invalid.
        """
        
        result = self.gateway.process_amount(-amount, user.id, description)
        if result:
            logger.info(f"Withdrawal of {amount} for user_id: {user.id}.")
        else:
            logger.error(f"Withdrawal of {amount} for user_id: {user.id} failed.")
        return result
        


        