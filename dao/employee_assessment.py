from sqlalchemy.orm import Session,joinedload
from models.employee_allocation import EmployeeAllocation
from models.assignment import QuestionAssignment
from models.questions import Question, Option
from models.self_assessment_response import SelfAssessmentResponse
from models.appraisal_cycle import AppraisalCycle
from models.stages import Stage
from models.employee import Employee
from sqlalchemy import or_, and_
from typing import List

# Get the cycle status
def get_cycle_status(db: Session, cycle_id: int) -> str:
    cycle = db.query(AppraisalCycle).filter(AppraisalCycle.cycle_id == cycle_id).first()
    return cycle.status if cycle else None

# Fetch the active(for which self assessment stage is either active or completed) and completed cycles for which employee is allocated
def get_allocated_cycles(db: Session, employee_id: int):
    return db.query(AppraisalCycle).join(EmployeeAllocation).join(Stage).filter(
        EmployeeAllocation.employee_id == employee_id,
        or_(
            AppraisalCycle.status == "completed",
            and_(
                AppraisalCycle.status == "active", 
                Stage.stage_name == "Self Assessment"  ,
                or_(
                    Stage.is_active == True,
                    Stage.is_completed == True
                )
            )
        )
    ).all()


# Fetch the active (for which self assessment stage is either active or completed)  and completed cycles  for which either the team lead or one of the employee under him is allocated 
def get_team_lead_cycles(db: Session, team_lead_id: int):
    # Step 1: Find all employees reporting to this team lead (including the team lead themselves)
    employee_ids = db.query(Employee.employee_id).filter(
        or_(
            Employee.reporting_manager == team_lead_id,
            Employee.employee_id == team_lead_id
        )
    ).all()
    
    # 'employee_ids' will be a list of tuples like [(1,), (2,), (3,)]
    employee_ids = [emp_id for (emp_id,) in employee_ids]

    # Step 2: Query cycles
    cycles = db.query(AppraisalCycle).join(EmployeeAllocation).join(Stage).filter(
        EmployeeAllocation.employee_id.in_(employee_ids),  # Allocation to any of the employee_ids
        or_(
            AppraisalCycle.status == "completed",  # Completed cycles
            and_(
                AppraisalCycle.status == "active",  # Active cycles
                Stage.stage_name == "Self Assessment",  # Only Self Assessment stage
                or_(
                    Stage.is_active == True,
                    Stage.is_completed == True
                )
            )
        )
    ).all()

    return cycles


# Fetch questions assigned to the employee for the selected active and completed cycles
def get_assigned_questions_with_options(db: Session, employee_id: int, cycle_id: int):
    # Get the allocation_id for the employee in this cycle
    allocation = db.query(EmployeeAllocation).filter_by(employee_id=employee_id, cycle_id=cycle_id).first()
    allocation_id = allocation.allocation_id if allocation else None

    # Get the questions and their options
    questions = db.query(Question).join(QuestionAssignment).options(
        joinedload(Question.options)
    ).filter(
        QuestionAssignment.employee_id == employee_id,
        QuestionAssignment.cycle_id == cycle_id
    ).all()

    # Attach allocation_id to each question (manually for now)
    for question in questions:
        question.allocation_id = allocation_id

    return questions



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
