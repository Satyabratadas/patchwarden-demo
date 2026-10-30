from demo_app.app.main import checkout
from demo_app.app.models import CheckoutRequest
from demo_app.app.store import reset_state


def setup_function() -> None:
    reset_state()


def test_unexpected_payment_response_leads_to_failed_order(monkeypatch):
    def fake_charge(amount: int, idempotency_key: str, provider_mode: str):
        if provider_mode == "malformed":
            # Simulate the malformed gateway payload that lacks the required 'status' field
            return {"unexpected": "gateway payload"}
        # For any other mode we return a minimal valid payload; the test only uses malformed.
        return {"status": "success", "charge_id": f"ch_{amount}"}

    monkeypatch.setattr("demo_app.app.payments.charge", fake_charge)

    request = CheckoutRequest(
        order_id="order-123",
        amount=50,
        idempotency_key="test-key",
        provider_mode="malformed",
    )
    # This call should raise a ValidationError before the fix.
    order = checkout(request)

    # After the fix the function should treat the missing status as a failed payment.
    assert order.status == "failed"
    assert order.charge_id is None
