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

    M_ID = Column(Integer, primary_key=True)
    GOAL = Column(String)
    HEALTH_METRIC = Column(String)

    # Member attends Class (many-to-one)
    C_ID = Column(Integer, ForeignKey("classes.C_ID"))
    attending_class = relationship("Class", back_populates="members")


# -------------------
# CLASS
# -------------------
class Class(Base):
    __tablename__ = "classes"

    C_ID = Column(Integer, primary_key=True)
    SIZE = Column(Integer)
    MAX_SIZE = Column(Integer)

    # Member attends Class (one-to-many)
    members = relationship("Member", back_populates="attending_class")

    # Trainer teaches Class (one-to-one)
    trainer = relationship("Trainer", back_populates="class_", uselist=False)

    # Classes are in Rooms (many-to-one)
    R_ID = Column(Integer, ForeignKey("rooms.R_ID"))
    room = relationship("Room", back_populates="classes")


# -------------------
# TRAINER
# -------------------
class Trainer(Base):
    __tablename__ = "trainers"

    T_ID = Column(Integer, primary_key=True)
    WORK_HOURS = Column(Integer)

    # One-to-one with Class
    C_ID = Column(Integer, ForeignKey("classes.C_ID"), unique=True)
    class_ = relationship("Class", back_populates="trainer")


# -------------------
# ROOM
# -------------------
class Room(Base):
    __tablename__ = "rooms"

    R_ID = Column(Integer, primary_key=True)

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

    id = Column(Integer, primary_key=True)
    TIME = Column(Integer)

    R_ID = Column(Integer, ForeignKey("rooms.R_ID"))
    room = relationship("Room", back_populates="bookings")


# -------------------
# EQUIPMENT
# -------------------
class Equipment(Base):
    __tablename__ = "equipment"

    id = Column(Integer, primary_key=True)
    TYPE = Column(String)
    STATUS = Column(String)
    COUNT = Column(Integer)

    R_ID = Column(Integer, ForeignKey("rooms.R_ID"))
    room = relationship("Room", back_populates="equipment")
