from sqlalchemy.orm import Session
from models.employee_allocation import EmployeeAllocation
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException

def assign_employee_to_cycle(db: Session, employee_id: int, cycle_id: int):
    """
    Add an employee-cycle pair to EmployeeAllocation if not already present.
    """
    try:
        existing_allocation = db.query(EmployeeAllocation).filter(
            EmployeeAllocation.employee_id == employee_id,
            EmployeeAllocation.cycle_id == cycle_id
        ).first()

        if existing_allocation:
            return [] # Already assigned, no need to add again

        new_allocation = EmployeeAllocation(employee_id=employee_id, cycle_id=cycle_id)
        db.add(new_allocation)
        db.commit()

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error during allocation: {str(e)}")

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")