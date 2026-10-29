from demo_app.app.main import checkout
from demo_app.app.models import CheckoutRequest
from demo_app.app.store import reset_state


def setup_function() -> None:
    reset_state()


def test_malformed_payment_response_leads_to_failed_order() -> None:
    # Simulate the production request that caused the ValidationError
    request = CheckoutRequest(
        order_id="order-123",
        amount=50,
        idempotency_key="test-key",
        provider_mode="malformed",
    )
    # This call should raise ValidationError before the fix.
    # After the fix, it should return a failed order instead of crashing.
    order = checkout(request)
    assert order.status == "failed"
    assert order.charge_id is None
