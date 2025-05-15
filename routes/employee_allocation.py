
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from database.connection import get_db
from models.employee_allocation import EmployeeAllocation
from typing import List

router = APIRouter(prefix="/employee-allocation", tags=["Employee Allocation"])

@router.get("/{cycle_id}", response_model=List[int])
def get_allocated_employees(cycle_id: int, db: Session = Depends(get_db)):
    try:
        employees = db.query(EmployeeAllocation.employee_id).filter(
            EmployeeAllocation.cycle_id == cycle_id
        ).all()

        if not employees:
            raise HTTPException(status_code=404, detail="No employees allocated to this cycle.")

        return [emp.employee_id for emp in employees]

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500,
            detail="Database error occurred"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred"
        )
