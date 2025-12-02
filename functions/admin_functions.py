import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from sqlalchemy.orm import Session
from models.models import Equipment, Class, Booking
import datetime

# -------------------
# ADMIN FUNCTIONS
# -------------------

def book_room_for_class(session: Session, class_id: int, room_id: int, booking_time: datetime):
    """Assign room for class and prevent double-booking."""
    # Check existing booking
    existing = session.query(Booking)\
        .filter(Class.room_id==room_id, Booking.TIME==booking_time)\
        .first()
    if existing:
        raise ValueError("Room already booked at this TIME")
    class_ = session.get(Class, class_id)
    if not class_:
        raise ValueError("Class not found")
    new_booking = Booking(
        class_id=class_id,
        room_id=room_id,
        TIME=booking_time
    )
    session.add(new_booking)
    session.commit()
    return class_


def log_equipment_issue(session: Session, equipment_id: int, status: str):
    """Update equipment status for maintenance."""
    equipment = session.get(Equipment, equipment_id)
    if not equipment:
        raise ValueError("Equipment not found")

    equipment.status = status

    session.commit()
    return equipment
