import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from sqlalchemy.orm import Session
from models.models import Member, Class
from datetime import date, time

# -------------------
# MEMBER FUNCTIONS
# -------------------

def register_member(session: Session, member_id: int, goal: str, health_metric: str):
    """Register a new member ensuring unique email."""
    if session.query(Member)\
        .filter(Member.member_id==member_id)\
        .first():
        raise ValueError("Member already registered")
    newMember = Member(
        member_id = member_id,
        goal = goal,
        health_metric = health_metric
    )
    session.add(newMember)
    session.commit()
    return newMember


def update_member_profile(session: Session, member_id: int, goal: str = "", health_metric: str = ""):
    """Update personal info."""
    member = session.get(Member, member_id)
    if not member:
        raise ValueError("Member not found")
    if goal == "": goal = member.goal
    if health_metric == "": health_metric = member.health_metric

    member.goal = goal
    member.health_metric = health_metric

    session.commit()
    return member


def member_dashboard(session: Session, member_id: int):
    """Return summary of latest health metrics, goals, and classes"""
    member = session.get(Member, member_id)
    if not member:
        raise ValueError("Member not found")

    print(f"Member {member.member_id} has goal '{member.goal}' and is {member.health_metric}\nClasses:")
    for c in member.attending_classes:
        print(f" - Class {c.class_id}, Trainer {c.trainer_id}, Room {c.room_id}")
    


def register_class(session: Session, member_id: int, class_id: int):

    member = session.get(Member, member_id)
    if not member:
        raise ValueError("Member not found")

    class_ = session.get(Class, class_id)
    if not class_:
        raise ValueError(f"Class not found")

    existing_registration = session.query(Member).join(Member.attending_classes).filter(
        Member.member_id == member_id,
        Class.class_id == class_id
    ).first()

    if existing_registration:
        raise ValueError(f"Member {member_id} is already registered for class {class_id}.")


    member.attending_classes.append(class_)
    session.commit()



