import pytest
from unittest.mock import patch, MagicMock
from app.payments import execute_payment, handle_stripe_webhook
from app.config import settings
import stripe

def test_execute_payment_simulation():
    """
    Test the execute_payment function in simulation mode.
    """
    settings.STRIPE_MODE = "simulation"
    
    # Valid amount
    success, tx_id, amount = execute_payment(10.0, "agent_1")
    assert success is True
    assert tx_id.startswith("tx_sim_")
    assert amount == 10.0

    # Invalid amount
    success, tx_id, amount = execute_payment(0.0, "agent_1")
    assert success is False
    assert tx_id is None
    assert amount == 0.0

def test_execute_payment_live_no_key():
    """
    Test live mode when STRIPE_SECRET_KEY is not configured.
    """
    settings.STRIPE_MODE = "live"
    settings.STRIPE_SECRET_KEY = ""
    
    success, tx_id, amount = execute_payment(5.0, "agent_2")
    assert success is False
    assert tx_id is None
    
    settings.STRIPE_MODE = "simulation"

@patch("stripe.PaymentIntent.create")
def test_execute_payment_live_success(mock_create):
    """
    Test live mode with a successful mocked Stripe PaymentIntent.
    """
    settings.STRIPE_MODE = "live"
    settings.STRIPE_SECRET_KEY = "sk_test_123"
    
    mock_intent = MagicMock()
    mock_intent.id = "pi_12345"
    mock_create.return_value = mock_intent
    
    success, tx_id, amount = execute_payment(2.5, "agent_3")
    assert success is True
    assert tx_id == "pi_12345"
    assert amount == 2.5
    mock_create.assert_called_once()
    
    settings.STRIPE_MODE = "simulation"
    settings.STRIPE_SECRET_KEY = ""

@patch("stripe.PaymentIntent.create")
def test_execute_payment_live_error(mock_create):
    """
    Test live mode when Stripe throws an error.
    """
    settings.STRIPE_MODE = "live"
    settings.STRIPE_SECRET_KEY = "sk_test_123"
    
    mock_create.side_effect = stripe.StripeError("Test error")
    
    success, tx_id, amount = execute_payment(2.5, "agent_3")
    assert success is False
    assert tx_id is None
    assert amount == 2.5
    
    settings.STRIPE_MODE = "simulation"
    settings.STRIPE_SECRET_KEY = ""

def test_handle_stripe_webhook_no_secret():
    """
    Test handle_stripe_webhook when STRIPE_WEBHOOK_SECRET is not configured.
    """
    settings.STRIPE_WEBHOOK_SECRET = ""
    assert handle_stripe_webhook(b"{}", "dummy_sig") is False

def test_handle_stripe_webhook_no_signature():
    """
    Test handle_stripe_webhook when signature header is missing.
    """
    settings.STRIPE_WEBHOOK_SECRET = "whsec_test"
    assert handle_stripe_webhook(b"{}", "") is False
    settings.STRIPE_WEBHOOK_SECRET = ""

@patch("stripe.Webhook.construct_event")
def test_handle_stripe_webhook_success(mock_construct):
    """
    Test handle_stripe_webhook with a valid signature and payload.
    """
    settings.STRIPE_WEBHOOK_SECRET = "whsec_test"
    
    # Mock a successful payment_intent.succeeded event
    mock_event = {
        "type": "payment_intent.succeeded",
        "data": {
            "object": {"id": "pi_123"}
        }
    }
    mock_construct.return_value = mock_event
    
    assert handle_stripe_webhook(b"{}", "valid_sig") is True
    
    # Mock a payment_intent.payment_failed event
    mock_event["type"] = "payment_intent.payment_failed"
    assert handle_stripe_webhook(b"{}", "valid_sig") is False
    
    # Mock an unhandled event
    mock_event["type"] = "charge.succeeded"
    assert handle_stripe_webhook(b"{}", "valid_sig") is True
    
    settings.STRIPE_WEBHOOK_SECRET = ""

@patch("stripe.Webhook.construct_event")
def test_handle_stripe_webhook_invalid_payload(mock_construct):
    """
    Test handle_stripe_webhook with an invalid payload (ValueError).
    """
    settings.STRIPE_WEBHOOK_SECRET = "whsec_test"
    mock_construct.side_effect = ValueError("Invalid payload")
    
    assert handle_stripe_webhook(b"invalid", "valid_sig") is False
    settings.STRIPE_WEBHOOK_SECRET = ""

@patch("stripe.Webhook.construct_event")
def test_handle_stripe_webhook_invalid_signature(mock_construct):
    """
    Test handle_stripe_webhook with an invalid signature.
    """
    settings.STRIPE_WEBHOOK_SECRET = "whsec_test"
    mock_construct.side_effect = stripe.error.SignatureVerificationError("Invalid sig", "sig", b"body")
    
    assert handle_stripe_webhook(b"{}", "invalid_sig") is False
    settings.STRIPE_WEBHOOK_SECRET = ""
