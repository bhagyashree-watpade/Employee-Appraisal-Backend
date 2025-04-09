from sqlalchemy.orm import Session,joinedload
from models.employee_allocation import EmployeeAllocation
from models.assignment import QuestionAssignment
from models.questions import Question, Option
from models.self_assessment_response import SelfAssessmentResponse
from models.appraisal_cycle import AppraisalCycle
from sqlalchemy import or_
from typing import List

# Get the cycle status
def get_cycle_status(db: Session, cycle_id: int) -> str:
    cycle = db.query(AppraisalCycle).filter(AppraisalCycle.cycle_id == cycle_id).first()
    return cycle.status if cycle else None

# Fetch the active and completed cycles for which employee is allocated
def get_allocated_cycles(db: Session, employee_id: int):
    return db.query(AppraisalCycle).join(EmployeeAllocation).filter(
        EmployeeAllocation.employee_id == employee_id,
        or_(AppraisalCycle.status == "active", AppraisalCycle.status == "completed")
    ).all()

# Fetch questions assigned to the employee for the selected active and completed cycles
def get_assigned_questions_with_options(db: Session, employee_id: int, cycle_id: int):
    return db.query(Question).join(QuestionAssignment).filter(
        QuestionAssignment.employee_id == employee_id,
        QuestionAssignment.cycle_id == cycle_id
    ).all()

# Fetch the reponses
def get_existing_responses(db: Session, employee_id: int, cycle_id: int):
    return (
        db.query(SelfAssessmentResponse)
        .options(
            joinedload(SelfAssessmentResponse.question),
            joinedload(SelfAssessmentResponse.option)
        )
        .filter(
            SelfAssessmentResponse.employee_id == employee_id,
            SelfAssessmentResponse.cycle_id == cycle_id
        )
        .all()
    )


# Save self assessment responses for the active cycles
def submit_self_assessment_responses(db: Session, responses: List[SelfAssessmentResponse]):
    db.add_all(responses)
    db.commit()
