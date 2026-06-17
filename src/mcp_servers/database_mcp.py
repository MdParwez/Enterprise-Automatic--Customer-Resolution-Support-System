from src.database.sqlite import fetch_all, fetch_one


class DatabaseMCP:
    def get_customer(self, customer_id: str) -> dict | None:
        return fetch_one("SELECT * FROM customers WHERE customer_id = ?", (customer_id,))

    def get_booking(self, customer_id: str) -> dict | None:
        return fetch_one("SELECT * FROM bookings WHERE customer_id = ? ORDER BY booking_id DESC LIMIT 1", (customer_id,))

    def get_refund(self, booking_id: str) -> dict | None:
        return fetch_one("SELECT * FROM refunds WHERE booking_id = ? ORDER BY refund_id DESC LIMIT 1", (booking_id,))

    def get_customer_history(self, customer_id: str) -> list[dict]:
        return fetch_all("SELECT * FROM tickets WHERE customer_id = ? ORDER BY created_at DESC", (customer_id,))
