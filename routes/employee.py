# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from typing import Optional,List
# from database.connection import get_db
# from services.employee import get_all_employees,get_sorted_employees
# # , get_filtered_employees, get_selected_columns
# from dao.employee import get_employees_under_manager, get_employee_details,get_employees_under_team_lead   #, get_reporting_employees
# from schema.employee import EmployeeResponse, EmployeeRoleResponse
# from models.employee import Employee
# router = APIRouter()

# @router.get("/")
# def read_employees_list(db:Session = Depends(get_db)):
#     return get_all_employees(db)

# @router.get("/reporting/{manager_id}")
# def get_reporting_employees(manager_id: int, db: Session = Depends(get_db)):
#     employees = get_employees_under_manager(db, manager_id)
#     if not employees:
#         raise HTTPException(status_code=404, detail="No employees found under this manager")
#     return employees

# @router.get("/reporting_manager/{employee_id}")
# def get_reporting_manager(employee_id: int, db: Session = Depends(get_db)):
#     # Get employee details from the database
#     employee = db.query(Employee).filter(Employee.employee_id == employee_id).first()

#     # If employee is not found
#     if not employee:
#         raise HTTPException(status_code=404, detail="Employee not found")

#     # If the employee doesn't have a reporting manager
#     if not employee.reporting_manager:  # Ensure the field name is correct
#         return {"reporting_manager_id": None, "reporting_manager_name": "No manager assigned"}

#     # Fetch reporting manager's details using the stored manager ID
#     manager = db.query(Employee).filter(Employee.employee_id == employee.reporting_manager).first()

#     # If no manager is found
#     if not manager:
#         return {"reporting_manager_id": None, "reporting_manager_name": "Manager not found"}

#     # Return both reporting manager's ID and name
#     return {
#         "reporting_manager_id": manager.employee_id,
#         "reporting_manager_name": manager.employee_name
#     }


# @router.get("/employee_details/{employee_id}", response_model=EmployeeRoleResponse)
# def get_employee(employee_id: int, db: Session = Depends(get_db)):
#     employee = get_employee_details(db, employee_id)
    
#     if not employee:
#         raise HTTPException(status_code=404, detail="Employee not found")

#     return employee

# @router.get("/employees/{cycle_id}/{team_lead_id}")
# def get_employees_for_cycle(cycle_id: int, team_lead_id: int, db: Session = Depends(get_db)):
#     employees = get_employees_under_team_lead(db, cycle_id, team_lead_id)
#     if not employees:
#         raise HTTPException(status_code=404, detail="No employees found for this cycle.")
#     return employees


# #historical report
# #get all the employees as per employee id in sorted manner
# @router.get("/employees", response_model=list[EmployeeResponse])
# def get_all_sorted_employees(db: Session = Depends(get_db)):
#     return get_sorted_employees(db)











from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional, List
from database.connection import get_db
from services.employee import get_all_employees, get_sorted_employees, fetch_employees_under_manager, fetch_reporting_manager, fetch_employee_details, fetch_employees_under_team_lead
from schema.employee import EmployeeResponse, EmployeeRoleResponse
from models.employee import Employee

router = APIRouter()
# router = APIRouter(prefix="/assessment", tags=["Self Assessment"])


@router.get("/")
def read_employees_list(db: Session = Depends(get_db)):
    try:
        return get_all_employees(db)
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error occurred while fetching employees.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/reporting/{manager_id}")
def get_reporting_employees(manager_id: int, db: Session = Depends(get_db)):
    try:
        employees = fetch_employees_under_manager(db, manager_id)
        if not employees:
            raise HTTPException(status_code=404, detail="No employees found under this manager")
        return employees
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error occurred while fetching employees under manager.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/reporting_manager/{employee_id}")
def get_reporting_manager(employee_id: int, db: Session = Depends(get_db)):
    try:
        result, error = fetch_reporting_manager(db, employee_id)
        if error == "Employee not found":
            raise HTTPException(status_code=404, detail=error)
        elif error in ["No manager assigned", "Manager not found"]:
            return {"reporting_manager_id": None, "reporting_manager_name": error}
        return result
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error occurred while fetching reporting manager.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/employee_details/{employee_id}", response_model=EmployeeRoleResponse)
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    try:
        employee, error = fetch_employee_details(db, employee_id)
        if error == "Employee not found":
            raise HTTPException(status_code=404, detail=error)
        return employee
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error occurred while fetching employee details.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/employees/{cycle_id}/{team_lead_id}")
def get_employees_for_cycle(cycle_id: int, team_lead_id: int, db: Session = Depends(get_db)):
    try:
        employees, error = fetch_employees_under_team_lead(db, cycle_id, team_lead_id)
        if error:
            raise HTTPException(status_code=404, detail=error)
        return employees
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error occurred while fetching employees for cycle.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Historical report: get all employees sorted
@router.get("/employees", response_model=List[EmployeeResponse])
def get_all_sorted_employees(db: Session = Depends(get_db)):
    try:
        return get_sorted_employees(db)
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error occurred while fetching sorted employees.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
