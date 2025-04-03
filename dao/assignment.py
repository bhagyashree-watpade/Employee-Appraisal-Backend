from sqlalchemy.orm import Session
from models.assignment import QuestionAssignment
from models.questions import Question

def assign_questions_to_employee(db: Session, employee_id: int, question_ids: list, cycle_id: int):
    # Fetch existing assignments to prevent duplicate entries
    existing_assignments = db.query(QuestionAssignment.question_id).filter(
        QuestionAssignment.employee_id == employee_id,
        QuestionAssignment.cycle_id == cycle_id,
        QuestionAssignment.question_id.in_(question_ids)
    ).all()

    # Extract already assigned question IDs
    assigned_question_ids = {q_id for (q_id,) in existing_assignments}

    # Filter out questions that are already assigned
    new_question_ids = [q_id for q_id in question_ids if q_id not in assigned_question_ids]

    if not new_question_ids:
        return []  # No new assignments needed

    # Insert only new assignments
    assignments = [
        QuestionAssignment(employee_id=employee_id, question_id=q_id, cycle_id=cycle_id)
        for q_id in new_question_ids
    ]
    db.add_all(assignments)
    db.commit()
    return assignments

def get_assignments_by_employee(db: Session, employee_id: int):
    return db.query(QuestionAssignment).filter(QuestionAssignment.employee_id == employee_id).all()

def get_assigned_questions(db: Session, employee_id: int, cycle_id: int):
    return (
        db.query(Question)
        .join(QuestionAssignment)
        .filter(
            QuestionAssignment.employee_id == employee_id,
            QuestionAssignment.cycle_id == cycle_id
        )
        .all()
    )
