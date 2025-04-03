from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.connection import get_db
from services.assignment import create_question_assignment, fetch_employee_assignments, fetch_assigned_questions
from schema.assignment import AssignmentCreate, AssignmentResponse
from typing import List
from models.employee_allocation import EmployeeAllocation

router = APIRouter(prefix="/assignments", tags=["Assignments"])

# @router.post("/", response_model=List[AssignmentResponse])
# def assign_questions(assignment_data: AssignmentCreate, db: Session = Depends(get_db)):
#     return create_question_assignment(db, assignment_data)

@router.post("/", response_model=List[AssignmentResponse])
def assign_questions(assignment_data: AssignmentCreate, db: Session = Depends(get_db)):
    print(assignment_data)
    return create_question_assignment(db, assignment_data)


@router.get("/{employee_id}", response_model=List[AssignmentResponse])
def get_assignments(employee_id: int, db: Session = Depends(get_db)):
    assignments = fetch_employee_assignments(db, employee_id)
    if not assignments:
        raise HTTPException(status_code=404, detail="No assignments found.")
    return assignments

@router.get("/{employee_id}/{cycle_id}")
def get_assigned_questions(employee_id: int, cycle_id: int, db: Session = Depends(get_db)):
    return fetch_assigned_questions(db, employee_id, cycle_id)


# @router.get("/{cycle_id}", response_model=List[int])  # Returns list of employee IDs
# def get_allocated_employees(cycle_id: int, db: Session = Depends(get_db)):
#     employees = db.query(EmployeeAllocation.employee_id).filter(
#         EmployeeAllocation.cycle_id == cycle_id
#     ).all()

#     if not employees:
#         raise HTTPException(status_code=404, detail="No employees allocated to this cycle.")

#     return [emp[0] for emp in employees]  # Extract employee IDs