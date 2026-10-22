from invoices import view_invoice


def test_returns_invoice() -> None:
    invoice = {"invoice_id": "inv-1", "owner_id": "user-a", "amount": 25}
    assert view_invoice(invoice, "user-a")["invoice_id"] == "inv-1"

