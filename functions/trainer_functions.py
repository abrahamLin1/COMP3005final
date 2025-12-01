from sqlalchemy.orm import Session
from models import Trainer, Member
from datetime import time

# -------------------
# TRAINER FUNCTIONS
# -------------------

def view_assigned_classes(session: Session, trainer_id: int):
    """Return all classes assigned to trainer."""
    trainer = session.get(Trainer, trainer_id)
    if not trainer:
        raise ValueError("Trainer not found")

    result = []
    for cls in trainer.classes:
        result.append({
            "class_id": cls.class_id,
            "room_id": cls.room_id
        })

    return result


def lookup_member(session: Session, member_id: int):


    member = session.get(Member, member_id)
    if not member:
        raise ValueError("Member not found")


    return {
        "member_id": member.member_id,
        "goal": member.goal,
        "health_metric_note": member.health_metric,
        "class_id": member.class_id
    }

