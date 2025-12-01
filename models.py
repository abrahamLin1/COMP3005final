from sqlalchemy import (
Column,
Integer,
String,
ForeignKey,
UniqueConstraint,
CheckConstraint,
DateTime,
Boolean,
func,
event,
Table,
Text,
)
from sqlalchemy.orm import relationship
from database import Base, engine


# -------------------
# MEMBER
# -------------------
class Member(Base):
    __tablename__ = "members"

    member_id = Column(Integer, primary_key=True)
    goal = Column(String)
    health_metric = Column(String)

    # Member attends Class (many-to-one)
    class_id = Column(Integer, ForeignKey("classes.class_id"))
    attending_class = relationship("Class", back_populates="members")


# -------------------
# CLASS
# -------------------
class Class(Base):
    __tablename__ = "classes"

    class_id = Column(Integer, primary_key=True)
    size = Column(Integer)
    max_size = Column(Integer)

    # Member attends Class (one-to-many)
    members = relationship("Member", back_populates="attending_class")

    # Trainer teaches Class (one-to-many)
    trainer_id = Column(Integer, ForeignKey("trainers.trainer_id"), nullable=False)
    trainer = relationship("Trainer", back_populates="classes")

    # Classes are in Rooms (many-to-one)
    room_id = Column(Integer, ForeignKey("rooms.room_id"))
    room = relationship("Room", back_populates="classes")

    bookings = relationship("Booking", back_populates="classes")


# -------------------
# TRAINER
# -------------------
class Trainer(Base):
    __tablename__ = "trainers"

    trainer_id = Column(Integer, primary_key=True)
    work_hours = Column(Integer)

    # One-to-Many: Trainer → Classes
    classes = relationship("Class", back_populates="trainer")


# -------------------
# ROOM
# -------------------
class Room(Base):
    __tablename__ = "rooms"

    room_id = Column(Integer, primary_key=True)

    # Classes are in rooms (one-to-many)
    classes = relationship("Class", back_populates="room")

    # Rooms have bookings (one-to-many)
    bookings = relationship("Booking", back_populates="room")

    # Rooms have equipment (one-to-many)
    equipment = relationship("Equipment", back_populates="room")


# -------------------
# BOOKING
# -------------------
class Booking(Base):
    __tablename__ = "bookings"

    booking_id = Column(Integer, primary_key=True)
    TIME = Column(DateTime)

    room_id = Column(Integer, ForeignKey("rooms.room_id"))
    class_id = Column(Integer, ForeignKey("classes.class_id"))
    room = relationship("Room", back_populates="bookings")
    classes = relationship("Class", back_populates="bookings")
    # One-to-many: booking → registrations
    registrations = relationship("Registration", back_populates="booking", cascade="all, delete-orphan")

# -------------------
# Register
# -------------------
class Registration(Base):
    __tablename__ = "registrations"

    registration_id = Column(Integer, primary_key=True)

    # Many-to-one FK → Booking
    booking_id = Column(Integer, ForeignKey("bookings.booking_id"), nullable=False)

    member_id = Column(Integer, ForeignKey("members.member_id"), nullable=False)

    booking = relationship("Booking", back_populates="registrations")


# -------------------
# EQUIPMENT
# -------------------
class Equipment(Base):
    __tablename__ = "equipment"

    equipment_id = Column(Integer, primary_key=True)
    type = Column(String)
    status = Column(String)

    room_id = Column(Integer, ForeignKey("rooms.room_id"))
    room = relationship("Room", back_populates="equipment")