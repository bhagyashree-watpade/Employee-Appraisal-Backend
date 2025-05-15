# from sqlalchemy.orm import Session
# from typing import Optional, List
# from dao.employee import fetch_all_employees,get_all_employees_sorted
# # filter_employees, fetch_columns

# def get_all_employees(db:Session):
#     return fetch_all_employees(db)
    
# #for historical report
# def get_sorted_employees(db: Session):
#     return get_all_employees_sorted(db)








from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional, List
from fastapi import HTTPException
from dao.employee import (
    fetch_all_employees, 
    get_all_employees_sorted , 
    get_employees_under_manager, 
    get_employee_by_id, 
    get_employee_manager, 
    get_employee_details, 
    get_employees_under_team_lead
)

def get_all_employees(db: Session):
    try:
        return fetch_all_employees(db)
    except HTTPException:
        raise
    
def get_sorted_employees(db: Session):
    try:
        return get_all_employees_sorted(db)
    except HTTPException:
        raise

def fetch_employees_under_manager(db: Session, manager_id: int):
    try:
        employees = get_employees_under_manager(db, manager_id)
        return employees
    except Exception as e:
        # Re-raise as needed or add custom logging here
        raise e

def fetch_reporting_manager(db: Session, employee_id: int):
    try:
        employee = get_employee_by_id(db, employee_id)
        if not employee:
            return None, "Employee not found"

        if not employee.reporting_manager:
            return None, "No manager assigned"

        manager = get_employee_manager(db, employee.reporting_manager)
        if not manager:
            return None, "Manager not found"

        return {
            "reporting_manager_id": manager.employee_id,
            "reporting_manager_name": manager.employee_name
        }, None
    except Exception as e:
        # Propagate exception up for route to handle
        raise e
    
def fetch_employee_details(db: Session, employee_id: int):
    try:
        employee_data = get_employee_details(db, employee_id)
        if not employee_data:
            return None, "Employee not found"
        return employee_data, None
    except Exception as e:
        # Propagate the exception to be handled by the route
        raise e
    
def fetch_employees_under_team_lead(db: Session, cycle_id: int, team_lead_id: int):
    try:
        employees = get_employees_under_team_lead(db, cycle_id, team_lead_id)
        if not employees:
            return None, "No employees found for this cycle."
        return employees, None
    except Exception as e:
        # Propagate the exception to be handled by the route
        raise e