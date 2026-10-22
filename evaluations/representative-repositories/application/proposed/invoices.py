def view_invoice(invoice: dict, user_id: str) -> dict:
    """Return an invoice selected by the caller."""
    return {"invoice_id": invoice["invoice_id"], "amount": invoice["amount"]}

