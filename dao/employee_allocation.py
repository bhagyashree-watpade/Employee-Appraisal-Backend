from sqlalchemy.orm import Session
from models.employee_allocation import EmployeeAllocation

def assign_employee_to_cycle(db: Session, employee_id: int, cycle_id: int):
    """
    Add an employee-cycle pair to Employee_allocation if not already present.
    """
    existing_allocation = db.query(EmployeeAllocation).filter(
        EmployeeAllocation.employee_id == employee_id,
        EmployeeAllocation.cycle_id == cycle_id
    ).first()

    if existing_allocation:
        return  # Already assigned, no need to add again

    new_allocation = EmployeeAllocation(employee_id=employee_id, cycle_id=cycle_id)
    db.add(new_allocation)
    db.commit()
