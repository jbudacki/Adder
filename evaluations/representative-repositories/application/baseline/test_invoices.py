from invoices import view_invoice


def test_rejects_non_owner() -> None:
    invoice = {"invoice_id": "inv-1", "owner_id": "user-a", "amount": 25}
    try:
        view_invoice(invoice, "user-b")
    except PermissionError:
        return
    raise AssertionError("non-owner access was not rejected")

