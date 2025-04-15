

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.connection import get_db
from services.parameter import fetch_all_parameters, fetch_parameter_by_id, create_parameter
from schema.parameter import ParameterCreate, ParameterResponse
from dao.parameter import get_parameters_for_cycle
from dao.employee import get_employee_by_id
from typing import List

router = APIRouter(prefix="/parameters", tags=["Parameters"])

@router.get("/", response_model=List[ParameterResponse])
def get_parameters(db: Session = Depends(get_db)):
    return fetch_all_parameters(db)

@router.get("/{parameter_id}", response_model=ParameterResponse)
def get_parameter(parameter_id: int, db: Session = Depends(get_db)):
    return fetch_parameter_by_id(db, parameter_id)

@router.post("/", response_model=ParameterResponse)
def add_parameter(parameter_data: ParameterCreate, db: Session = Depends(get_db)):
    return create_parameter(db, parameter_data)


@router.get("/{cycle_id}/{employee_id}")
def fetch_parameters(cycle_id: int, employee_id: int, db: Session = Depends(get_db)):
    """Fetch appraisal parameters for a given cycle and employee role"""

    # Fetch employee details
    employee = get_employee_by_id(db, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    # Determine if employee is a lead
    is_lead = employee.role.lower() == "team lead"

    # Fetch parameters based on role
    parameters = get_parameters_for_cycle(db, cycle_id, is_lead)

    return parameters  # Return as a list, not inside an object
