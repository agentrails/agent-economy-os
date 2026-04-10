"""
Universal Agent Economy OS - Native x402 Middleware

This module provides the middleware layer for x402 micropayments. It intercepts
requests, checks if the target tool or agent requires a payment, verifies the
provided payment amount, and returns an HTTP 402 Payment Required response
with clear instructions if the payment is missing or insufficient.
"""
import logging
from typing import Tuple, Optional, Any, Dict
from app.errors import PaymentRequiredError, PaymentFailedError
from app.payments import execute_payment

logger = logging.getLogger(__name__)

def process_x402_payment(agent_id: str, tool_call: Dict[str, Any], payment_amount: Optional[float]) -> Tuple[bool, Optional[str]]:
    """
    Native x402 middleware logic.
    
    1. Checks if the tool call requires a payment (e.g., via a 'required_payment' field).
    2. Verifies that the provided payment_amount is sufficient.
    3. If insufficient or missing, raises a 402 PaymentRequiredError.
    4. If sufficient, executes the payment via the settlement engine.
    
    Returns:
        Tuple[bool, Optional[str]]: (settled_status, transaction_id)
    """
    # Determine the required payment amount from the tool call payload.
    # In a fully dynamic system, this could be fetched from a registry or the target agent.
    # For now, we check if the tool call explicitly asks for a required payment.
    required_payment = float(tool_call.get("required_payment", 0.0))
    provided_amount = float(payment_amount) if payment_amount is not None else 0.0
    
    # Check if payment is required but not provided or insufficient
    if required_payment > 0.0 and provided_amount < required_payment:
        logger.warning(f"Agent {agent_id} provided insufficient payment ({provided_amount}) for required {required_payment}.")
        raise PaymentRequiredError(required_amount=required_payment)
        
    # If a payment is provided (even optionally), process it
    if provided_amount > 0.0:
        logger.info(f"Processing x402 payment of {provided_amount} for agent {agent_id}.")
        settled, transaction_id, _ = execute_payment(provided_amount, agent_id)
        
        if not settled:
            logger.error(f"x402 payment settlement failed for agent {agent_id}.")
            raise PaymentFailedError("Payment settlement failed during x402 middleware processing.")
            
        return True, transaction_id
        
    # No payment required and no payment provided
    return False, None
