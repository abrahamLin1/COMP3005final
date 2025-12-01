from database import Base, engine, SessionLocal
from models import Member, Class, Trainer, Room, Booking, Equipment
import functions.admin_functions as a_f
import functions.member_functions as m_f
import functions.trainer_functions as t_f
import datetime

def init_db():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Done.")


def seed_data():
    session = SessionLocal()

    # ---------------------------
    # Create Rooms
    # ---------------------------
    room1 = Room(room_id=1)
    room2 = Room(room_id=2)

    # ---------------------------
    # Create Trainers
    # ---------------------------
    trainer1 = Trainer(trainer_id=201, work_hours=40)
    trainer2 = Trainer(trainer_id=202, work_hours=35)

    session.add_all([trainer1, trainer2])
    session.commit()

    session.add_all([room1, room2])
    session.commit()

    # ---------------------------
    # Create Classes
    # ---------------------------
    class1 = Class(class_id=101, size=10, max_size=20, trainer=trainer1, room=room1)
    class2 = Class(class_id=102, size=5, max_size=10, trainer=trainer2, room=room2)

    session.add_all([class1, class2])
    session.commit()

    # ---------------------------
    # Create Members
    # ---------------------------
    member1 = Member(member_id=301, goal="Lose Weight", health_metric="Good", attending_class=class1)
    member2 = Member(member_id=302, goal="Build Muscle", health_metric="Excellent", attending_class=class1)
    member3 = Member(member_id=303, goal="Endurance", health_metric="Fair", attending_class=class2)

    session.add_all([member1, member2, member3])
    session.commit()

    # ---------------------------
    # Create Bookings (room → many bookings)
    # ---------------------------
    booking1 = Booking(TIME=datetime.date(2025,12,11), classes = class1, room=room1)
    booking2 = Booking(TIME=datetime.date(2025,12,12), classes = class1, room=room1)
    booking3 = Booking(TIME=datetime.date(2025,12,13), classes = class2, room=room2)

    session.add_all([booking1, booking2, booking3])
    session.commit()

    # ---------------------------
    # Create Equipment (room → many equipment pieces)
    # ---------------------------
    eq1 = Equipment(equipment_id = 1, type="Treadmill", status="Working", room=room1)
    eq2 = Equipment(equipment_id = 2, type="Dumbbells", status="Good",  room=room1)
    eq3 = Equipment(equipment_id = 3, type="Bike", status="Needs Service", room=room2)

    session.add_all([eq1, eq2, eq3])
    session.commit()

    session.close()
    print("Seed data inserted.")


def print_summary():
    session = SessionLocal()

    print("\n=== Classes and Members ===")
    for c in session.query(Class).all():
        print(f"Class {c.class_id} in Room {c.room_id} has members:")
        for m in c.members:
            print(f" - {m.member_id}: {m.goal}")

    print("\n=== Trainers (One-to-One) ===")
    for t in session.query(Trainer).all():
        print(f"Trainer {t.trainer_id} teaches Classes: {[cls.class_id for cls in t.classes]}")

    print("\n=== Rooms, Bookings, and Equipment ===")
    for r in session.query(Room).all():
        print(f"Room {r.room_id}:")
        print("  Bookings:")
        for b in r.bookings:
            print(f"   - Time {b.TIME}, Class {b.class_id}, Room {b.room_id}")
        print("  Equipment:")
        for e in r.equipment:
            print(f"   -ID: {e.equipment_id} {e.type} Status: {e.status}")

    session.close()

def print_dictionary(result):
    print("Assigned classes:")
    for item in result:
        print(f"    -Class ID: {item['class_id']}, Room ID: {item['room_id']}")

if __name__ == "__main__":
    try:
        init_db()
        #seed_data() # Only need to run this once when database is empty
        #a_f.book_room_for_class(session=SessionLocal(), class_id=101, room_id=2, booking_time=datetime.date(2021, 12, 30))
        #a_f.log_equipment_issue(session=SessionLocal(), equipment_id=1, status="Broken")
        #print_dictionary(t_f.view_assigned_classes(session=SessionLocal(), trainer_id=202))
        #print(t_f.lookup_member(session=SessionLocal(), member_id=302))
        #print_summary()

    except ValueError as e:
        print(e)