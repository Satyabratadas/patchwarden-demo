from demo_app.app.main import checkout
from demo_app.app.models import CheckoutRequest
from demo_app.app.store import reset_state


def setup_function() -> None:
    reset_state()


def test_malformed_payment_response_results_in_failed_order() -> None:
    # Simulate the production scenario where the gateway returns a payload
    # missing the required 'status' field when provider_mode is "malformed".
    order = checkout(
        CheckoutRequest(
            order_id="order-123",
            amount=50,
            idempotency_key="test-key",
            provider_mode="malformed",
        )
    )
    # After fixing the bug, the endpoint should treat the malformed response
    # as a declined payment and return an order with status "failed".
    assert order.status == "failed"
    assert order.charge_id is None
