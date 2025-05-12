from sqlalchemy.orm import Session, aliased
from typing import Optional,List
from models.employee import Employee
from models.employee_allocation import  EmployeeAllocation

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
    
    
def get_reporting_employees(db: Session, reporting_manager_id: int) -> List[Employee]:
    """Fetch employees who report to a specific manager."""
    return db.query(Employee).filter(Employee.reporting_manager == reporting_manager_id).all()


#for getting reporting manager name of the selected employee
def get_reporting_manager(db: Session, employee_id: int) -> Optional[str]:
    """Fetch the reporting manager's name for a given employee."""
    employee = db.query(Employee).filter(Employee.employee_id == employee_id).first()
    if employee and employee.reporting_manager:
        manager = db.query(Employee).filter(Employee.employee_id == employee.reporting_manager).first()
        return manager.employee_name if manager else None
    return None


def get_employee_details(db: Session, employee_id: int):
    employee = db.query(Employee).filter(Employee.employee_id == employee_id).first()
    
    if not employee:
        return None  # Employee not found
    
    # Fetch reporting manager details if exists
    # reporting_manager = db.query(Employee).filter(Employee.employee_id == employee.reporting_manager).first()

    return {
        # "employee_id": employee.employee_id,
        # "employee_name": employee.employee_name,
        "role": employee.role
        # "reporting_manager": reporting_manager.employee_name if reporting_manager else None
    }


def get_employees_under_team_lead(db: Session, cycle_id: int, team_lead_id: int):
    # Fetch employees under the team lead for the selected cycle
    employees = db.query(Employee).join(
        EmployeeAllocation, Employee.employee_id == EmployeeAllocation.employee_id
    ).filter(
        EmployeeAllocation.cycle_id == cycle_id,
        Employee.reporting_manager == team_lead_id
    ).all()

    # Fetch team lead details separately (ensure they are included)
    team_lead = db.query(Employee).filter(Employee.employee_id == team_lead_id).first()

    # Combine team lead with employees and remove duplicates (if any)
    if team_lead and team_lead not in employees:
        employees.append(team_lead)

    return employees

#for historical report

def get_all_employees_sorted(db: Session):
    manager = aliased(Employee)
    prev_manager = aliased(Employee)

    result = db.query(
        Employee.employee_id,
        Employee.employee_name,
        Employee.role,
        manager.employee_name.label("reporting_manager_name"),
        prev_manager.employee_name.label("previous_reporting_manager_name")
    ).outerjoin(
        manager, Employee.reporting_manager == manager.employee_id
    ).outerjoin(
        prev_manager, Employee.previous_reporting_manager == prev_manager.employee_id
    ).order_by(Employee.employee_id).all()

    return result


#to get employee by role id
def get_employee_by_role_id(db: Session, role_id: str):
    """Fetch employee by role ID."""
    return db.query(Employee).filter(Employee.role_id == role_id).first()
