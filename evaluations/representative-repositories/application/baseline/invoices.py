def view_invoice(invoice: dict, user_id: str) -> dict:
    """Return an invoice only to its owning user."""
    if invoice["owner_id"] != user_id:
        raise PermissionError("invoice access denied")
    return {"invoice_id": invoice["invoice_id"], "amount": invoice["amount"]}

