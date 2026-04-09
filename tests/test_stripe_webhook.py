import os

# Set dummy environment variables for testing before importing the app
os.environ["API_KEY"] = "test_api_key"
os.environ["SUPABASE_URL"] = ""
os.environ["SUPABASE_KEY"] = ""
os.environ["ALLOWED_ORIGINS"] = '["*"]'
os.environ["WEBHOOK_SECRET"] = "test_secret"

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_stripe_webhook_endpoint_success():
    """
    Test the /webhooks/stripe endpoint with a valid signature and payload.
    """
    from unittest.mock import patch
    from app.config import settings
    
    settings.STRIPE_WEBHOOK_SECRET = "whsec_test"
    
    with patch("app.main.handle_stripe_webhook", return_value=True):
        response = client.post(
            "/webhooks/stripe",
            content=b"{}",
            headers={"Stripe-Signature": "valid_sig"}
        )
        assert response.status_code == 200
        assert response.json() == {"status": "received"}
        
    settings.STRIPE_WEBHOOK_SECRET = ""

def test_stripe_webhook_endpoint_missing_signature():
    """
    Test the /webhooks/stripe endpoint with missing signature.
    """
    response = client.post(
        "/webhooks/stripe",
        content=b"{}"
    )
    assert response.status_code == 400
    assert response.json()["error_code"] == "MISSING_SIGNATURE"

def test_stripe_webhook_endpoint_invalid_signature():
    """
    Test the /webhooks/stripe endpoint with an invalid signature (handler returns False).
    """
    from unittest.mock import patch
    from app.config import settings
    
    settings.STRIPE_WEBHOOK_SECRET = "whsec_test"
    
    with patch("app.main.handle_stripe_webhook", return_value=False):
        response = client.post(
            "/webhooks/stripe",
            content=b"{}",
            headers={"Stripe-Signature": "invalid_sig"}
        )
        assert response.status_code == 400
        assert response.json()["error_code"] == "INVALID_WEBHOOK"
        
    settings.STRIPE_WEBHOOK_SECRET = ""
