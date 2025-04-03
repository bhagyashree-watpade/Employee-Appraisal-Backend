from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.connection import get_db
from models.employee_allocation import EmployeeAllocation
from typing import List

router = APIRouter(prefix="/employee-allocation", tags=["Employee Allocation"])


@router.get("/{cycle_id}", response_model=List[int])  # Returns list of employee IDs
def get_allocated_employees(cycle_id: int, db: Session = Depends(get_db)):
    employees = db.query(EmployeeAllocation.employee_id).filter(
        EmployeeAllocation.cycle_id == cycle_id
    ).all()

    if not employees:
        raise HTTPException(status_code=404, detail="No employees allocated to this cycle.")

    return [emp.employee_id for emp in employees]  # ✅ Access the attribute directly
