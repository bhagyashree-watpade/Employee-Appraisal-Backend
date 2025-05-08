from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional,List
from database.connection import get_db
from services.employee import get_all_employees,get_sorted_employees
# , get_filtered_employees, get_selected_columns
from dao.employee import get_employees_under_manager, get_employee_details,get_employees_under_team_lead   #, get_reporting_employees
from schema.employee import EmployeeResponse, EmployeeRoleResponse
from models.employee import Employee
router = APIRouter()

@router.get("/")
def read_employees_list(db:Session = Depends(get_db)):
    return get_all_employees(db)

@router.get("/reporting/{manager_id}")
def get_reporting_employees(manager_id: int, db: Session = Depends(get_db)):
    employees = get_employees_under_manager(db, manager_id)
    if not employees:
        raise HTTPException(status_code=404, detail="No employees found under this manager")
    return employees

@router.get("/reporting_manager/{employee_id}")
def get_reporting_manager(employee_id: int, db: Session = Depends(get_db)):
    # Get employee details from the database
    employee = db.query(Employee).filter(Employee.employee_id == employee_id).first()

    # If employee is not found
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    # If the employee doesn't have a reporting manager
    if not employee.reporting_manager:  # Ensure the field name is correct
        return {"reporting_manager_id": None, "reporting_manager_name": "No manager assigned"}

    # Fetch reporting manager's details using the stored manager ID
    manager = db.query(Employee).filter(Employee.employee_id == employee.reporting_manager).first()

    # If no manager is found
    if not manager:
        return {"reporting_manager_id": None, "reporting_manager_name": "Manager not found"}

    # Return both reporting manager's ID and name
    return {
        "reporting_manager_id": manager.employee_id,
        "reporting_manager_name": manager.employee_name
    }


@router.get("/employee_details/{employee_id}", response_model=EmployeeRoleResponse)
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = get_employee_details(db, employee_id)
    
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    return employee

@router.get("/employees/{cycle_id}/{team_lead_id}")
def get_employees_for_cycle(cycle_id: int, team_lead_id: int, db: Session = Depends(get_db)):
    employees = get_employees_under_team_lead(db, cycle_id, team_lead_id)
    if not employees:
        raise HTTPException(status_code=404, detail="No employees found for this cycle.")
    return employees


#historical report
#get all the employees as per employee id in sorted manner
@router.get("/employees", response_model=list[EmployeeResponse])
def get_all_sorted_employees(db: Session = Depends(get_db)):
    return get_sorted_employees(db)
