from sqlalchemy.orm import Session
from dao.employee import get_employee_by_id, get_employee_by_role_id

def authenticate_employee(db: Session, employee_id: int, password: str):
    """Authenticate employee by checking if the provided password matches the stored one."""
    # employee = get_employee_by_id(db, employee_id)     # for login based on employee ID
    employee = get_employee_by_role_id(db, employee_id) # for login based on role ID

    if not employee:
        return None  # Employee not found
    
    if employee.password != password:
        return None  # Password mismatch
    
    return employee  # Successful authentication
