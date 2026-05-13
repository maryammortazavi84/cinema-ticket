from datetime import datetime
from decimal import Decimal
from core.ticket import Ticket


def test_create_ticket_success():
    ticket = Ticket(
        ticket_id=None,
        user_id="user123",
        showtime_id="show1",
        seat_row="A",
        seat_number=10,
        price=Decimal("12.50"),
        booked_at=datetime.now()
    )

    assert ticket.user_id == "user123"
    assert ticket.showtime_id == "show1"
    assert ticket.seat_row == "A"
    assert ticket.seat_number == 10
    assert ticket.price == Decimal("12.50")