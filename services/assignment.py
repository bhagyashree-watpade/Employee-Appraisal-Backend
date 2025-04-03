from sqlalchemy.orm import Session
from models.assignment import QuestionAssignment
# from models.employee_allocation import EmployeeAllocation 
from dao.employee_allocation import assign_employee_to_cycle  
from schema.assignment import AssignmentCreate, AssignmentResponse
from collections import defaultdict


# def create_question_assignment(db: Session, assignment_data: AssignmentCreate):
#     new_assignments = []

#     for employee_id in assignment_data.employee_ids:  # ✅ Loop through multiple employees
#         for question_id in assignment_data.question_ids:
#             new_assignments.append(
#                 QuestionAssignment(
#                     employee_id=employee_id,
#                     cycle_id=assignment_data.cycle_id,
#                     question_id=question_id
#                 )
#             )

#     db.add_all(new_assignments)
#     db.commit()

#     return [
#         AssignmentResponse(
#             employee_id=employee_id,
#             cycle_id=assignment_data.cycle_id,
#             question_ids=assignment_data.question_ids
#         ) for employee_id in assignment_data.employee_ids
#     ]


def create_question_assignment(db: Session, assignment_data: AssignmentCreate):
    new_assignments = []

    for employee_id in assignment_data.employee_ids:
        # ✅ Call function to ensure employee is assigned to the cycle
        assign_employee_to_cycle(db, employee_id, assignment_data.cycle_id)

        # ✅ Now, assign questions
        for question_id in assignment_data.question_ids:
            new_assignments.append(
                QuestionAssignment(
                    employee_id=employee_id,
                    cycle_id=assignment_data.cycle_id,
                    question_id=question_id
                )
            )

    db.add_all(new_assignments)
    db.commit()

    return [
        AssignmentResponse(
            employee_id=employee_id,
            cycle_id=assignment_data.cycle_id,
            question_ids=assignment_data.question_ids
        ) for employee_id in assignment_data.employee_ids
    ]
    

def fetch_employee_assignments(db: Session, employee_id: int):
    """
    Retrieve all assignments for an employee, grouping questions by cycle.
    """
    assignments = db.query(QuestionAssignment).filter(
        QuestionAssignment.employee_id == employee_id
    ).all()

    # ✅ Group assignments by cycle_id
    grouped_assignments = defaultdict(lambda: {"employee_id": employee_id, "cycle_id": None, "question_ids": []})

    for assignment in assignments:
        grouped_assignments[assignment.cycle_id]["cycle_id"] = assignment.cycle_id
        grouped_assignments[assignment.cycle_id]["question_ids"].append(assignment.question_id)

    return [AssignmentResponse(**data) for data in grouped_assignments.values()]

def fetch_assigned_questions(db: Session, employee_id: int, cycle_id: int):
    """
    Fetch questions assigned to an employee for a specific appraisal cycle.
    """
    assignments = db.query(QuestionAssignment).filter(
        QuestionAssignment.employee_id == employee_id,
        QuestionAssignment.cycle_id == cycle_id
    ).all()

    # ✅ Extract only question IDs
    question_ids = [assignment.question_id for assignment in assignments]

    return AssignmentResponse(
        employee_id=employee_id,
        cycle_id=cycle_id,
        question_ids=question_ids
    )


