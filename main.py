from database import Base, engine, SessionLocal
from models import Member, Class, Trainer, Room, Booking, Equipment


def init_db():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Done.")


def seed_data():
    session = SessionLocal()

    # ---------------------------
    # Create Rooms
    # ---------------------------
    room1 = Room(R_ID=1)
    room2 = Room(R_ID=2)

    session.add_all([room1, room2])
    session.commit()

    # ---------------------------
    # Create Classes
    # ---------------------------
    class1 = Class(C_ID=101, SIZE=10, MAX_SIZE=20, room=room1)
    class2 = Class(C_ID=102, SIZE=5, MAX_SIZE=10, room=room2)

    session.add_all([class1, class2])
    session.commit()

    # ---------------------------
    # Create Trainers (1-to-1)
    # ---------------------------
    trainer1 = Trainer(T_ID=201, WORK_HOURS=40, class_=class1)
    trainer2 = Trainer(T_ID=202, WORK_HOURS=35, class_=class2)

    session.add_all([trainer1, trainer2])
    session.commit()

    # ---------------------------
    # Create Members (many-to-one)
    # ---------------------------
    member1 = Member(M_ID=301, GOAL="Lose Weight", HEALTH_METRIC="Good", attending_class=class1)
    member2 = Member(M_ID=302, GOAL="Build Muscle", HEALTH_METRIC="Excellent", attending_class=class1)
    member3 = Member(M_ID=303, GOAL="Endurance", HEALTH_METRIC="Fair", attending_class=class2)

    session.add_all([member1, member2, member3])
    session.commit()

    # ---------------------------
    # Create Bookings (room → many bookings)
    # ---------------------------
    booking1 = Booking(TIME=9, room=room1)
    booking2 = Booking(TIME=14, room=room1)
    booking3 = Booking(TIME=11, room=room2)

    session.add_all([booking1, booking2, booking3])
    session.commit()

    # ---------------------------
    # Create Equipment (room → many equipment pieces)
    # ---------------------------
    eq1 = Equipment(TYPE="Treadmill", STATUS="Working", COUNT=5, room=room1)
    eq2 = Equipment(TYPE="Dumbbells", STATUS="Good", COUNT=20, room=room1)
    eq3 = Equipment(TYPE="Bike", STATUS="Needs Service", COUNT=3, room=room2)

    session.add_all([eq1, eq2, eq3])
    session.commit()

    session.close()
    print("Seed data inserted.")


def print_summary():
    session = SessionLocal()

    print("\n=== Classes and Members ===")
    for c in session.query(Class).all():
        print(f"Class {c.C_ID} in Room {c.R_ID} has members:")
        for m in c.members:
            print(f" - {m.M_ID}: {m.GOAL}")

    print("\n=== Trainers (One-to-One) ===")
    for t in session.query(Trainer).all():
        print(f"Trainer {t.T_ID} teaches Class {t.C_ID}")

    print("\n=== Rooms, Bookings, and Equipment ===")
    for r in session.query(Room).all():
        print(f"Room {r.R_ID}:")
        print("  Bookings:")
        for b in r.bookings:
            print(f"   - Time {b.TIME}")
        print("  Equipment:")
        for e in r.equipment:
            print(f"   - {e.TYPE} ({e.COUNT}) Status: {e.STATUS}")

    session.close()


if __name__ == "__main__":
    init_db()
    #seed_data()
    print_summary()
