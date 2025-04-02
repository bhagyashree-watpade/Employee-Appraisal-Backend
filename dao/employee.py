from sqlalchemy.orm import Session
from typing import Optional,List
from models.employee import Employee

def fetch_all_employees(db:Session):
    employees_list = db.query(Employee).all()
    return employees_list


#new
def get_employee_by_id(db: Session, employee_id: int):
    return db.query(Employee).filter(Employee.employee_id == employee_id).first()


#for getting employee under team lead
def get_employees_by_manager(db: Session, manager_id: int):
    """Fetch employees where the given employee is the reporting manager."""
    return db.query(Employee).filter((Employee.reporting_manager == manager_id) | (Employee.employee_id == manager_id)).all()

def get_employees_under_manager(db: Session, manager_id: int):
    """Fetch employees where the given employee is the reporting manager, including themselves."""
    return db.query(Employee).filter(
        (Employee.reporting_manager == manager_id) | (Employee.employee_id == manager_id)
    ).all()