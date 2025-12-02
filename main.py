import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database import Base, engine, SessionLocal
from models.models import Member, Class, Trainer, Room, Booking, Equipment
import functions.admin_functions as a_f
import functions.member_functions as m_f
import functions.trainer_functions as t_f
import datetime
from datetime import datetime
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
    class1 = Class(class_id=101, max_size=20, trainer=trainer1, room=room1)
    class2 = Class(class_id=102, max_size=10, trainer=trainer2, room=room2)

    session.add_all([class1, class2])
    session.commit()

    # ---------------------------
    # Create Members
    # ---------------------------
    member1 = Member(member_id=301, goal="Lose Weight", health_metric="Good", attending_classes=[class1, class2])
    member2 = Member(member_id=302, goal="Build Muscle", health_metric="Excellent", attending_classes=[class1])
    member3 = Member(member_id=303, goal="Endurance", health_metric="Fair", attending_classes=[class2])

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

    print("\n=== Members ===")
    for m in session.query(Member).all():
        print(f"Member {m.member_id} has goal '{m.goal}' and is {m.health_metric}")

    print("\n=== Classes and Members ===")
    for c in session.query(Class).all():
        print(f"Class {c.class_id} in Room {c.room_id} has members:")
        for m in c.members:
            print(f" - {m.member_id}")

    print("\n=== Trainers (One-to-One) ===")
    for t in session.query(Trainer).all():
        print(f"Trainer {t.trainer_id} teaches Classes: {[cls.class_id for cls in t.classes]}")

    print("\n=== Rooms, Bookings, and Equipment ===")
    for r in session.query(Room).all():
        print(f"Room {r.room_id}:")
        print("  Bookings:")
        for b in r.bookings:
            print(f"   - ID: {b.booking_id} Time {b.TIME}, Class {b.class_id}, Room {b.room_id}")
        print("  Equipment:")
        for e in r.equipment:
            print(f"   - ID: {e.equipment_id} {e.type} Status: {e.status}")

    session.close()

def print_dictionary(result):
    print("Assigned classes:")
    for item in result:
        print(f"    -Class ID: {item['class_id']}, Room ID: {item['room_id']}")

if __name__ == "__main__":
    
        try:
            init_db()
            #seed_data() # Only need to run this once when database is empty
            userInput = int(input("Are you a Member(1), Trainer(2), or Admin(3). 0 to exit"))

            while True:
                match userInput:
                    
                    case 0:
                        break
                    case 1:
                        newInput = int(input("Would you like to Register a new member(1), Update an existing member(2), Show a member's dashboard(3), or Register for a class(4). 0 to exit"))
                        match newInput:
                            case 0:
                                break
                            case 1:
                                mid = int(input("Enter a Member ID: "))
                                g = input("Enter a Goal(str): ")
                                hm = input("Enter a Health Metric(str): ")
                                m_f.register_member(session=SessionLocal(), member_id= mid, goal = g, health_metric= hm)
                            case 2:
                                mid = int(input("Enter a Member ID: "))
                                g = input("Enter a Goal(str): ")
                                hm = input("Enter a Health Metric(str): ")
                                m_f.update_member_profile(session=SessionLocal(), member_id= mid, goal = g, health_metric= hm)
                            case 3:
                                mid = int(input("Enter a Member ID: "))
                                m_f.member_dashboard(session=SessionLocal(), member_id=mid)
                            case 4:
                                mid = int(input("Enter a Member ID: "))
                                cid = int(input("Enter a Class ID: "))
                                m_f.register_class(session=SessionLocal(), member_id=mid, class_id=cid)
    
                        #print_summary() # For debugging
                    case 2:
                        newInput = int(input("Would you like to View assigned classes(1) or Lookup a member(2)? 0 to exit"))
                        match newInput:
                            case 0:
                                break
                            case 1:
                                tid = int(input("Input trainer ID: "))
                                print_dictionary(t_f.view_assigned_classes(session=SessionLocal(), trainer_id=tid))
                            case 2:
                                mid = int(input("Enter a Member ID: "))
                                temp = t_f.lookup_member(session=SessionLocal(), member_id=mid)
                                print(f'Member {temp["member_id"]} has goal "{temp["goal"]}" and is {temp["health_metric"]}\nClasses')

                                for c in temp["classes"]:
                                    print(f" - Class {c.class_id}, Trainer {c.trainer_id}, Room {c.room_id}")
                        #print_summary() # For debuggings
                    case 3:
                        newInput = int(input("Would you like to Book a room for class(1), Log equipment issues(2), or Print summary(3). 0 to exit"))
                        match newInput:
                            case 0:
                                break
                            case 1:
                                cid = int(input("Input class ID: "))
                                rid = int(input("Input room ID: "))
                                d = input("Input a date (YYYY-MM-DD):")
                                d = datetime.strptime(d, "%Y-%m-%d").date()
                                a_f.book_room_for_class(session=SessionLocal(), class_id=cid, room_id=rid, booking_time=d)
                            case 2:
                                eid = int(input("Input equipment ID: "))
                                s = input("Input status(str): ")
                                a_f.log_equipment_issue(session=SessionLocal(), equipment_id=eid, status=s)
                            case 3:
                                print_summary()
                        #print_summary() # debugs

        except ValueError as e:
            print(e)