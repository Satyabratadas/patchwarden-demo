from demo_app.app.main import checkout
from demo_app.app.models import CheckoutRequest
from demo_app.app.store import reset_state
import demo_app.app.payments as payments

def setup_function() -> None:
    reset_state()


def test_malformed_gateway_response_results_in_failed_order(monkeypatch) -> None:
    # Ensure clean state
    reset_state()
    request = CheckoutRequest(
        order_id="order-123",
        amount=50,
        idempotency_key="key-123",
        provider_mode="malformed",
        sku="sku-basic",
    )
    def fake_charge(amount: int, idempotency_key: str, provider_mode: str) -> dict:
        # Simulate the malformed gateway payload that lacks the required 'status' field
        return {"unexpected": "gateway payload"}
    monkeypatch.setattr(payments, "charge", fake_charge)
    # This call should raise a ValidationError today; after the bug is fixed it will
    # return an Order representing a failed payment.
    order = checkout(request)
    assert order.status == "failed"
    assert order.charge_id is None
