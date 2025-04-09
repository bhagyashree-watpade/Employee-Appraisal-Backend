

from sqlalchemy.orm import Session
from dao.parameter import get_all_parameters, get_parameter_by_id, add_parameter, get_parameter_id_by_name
from schema.parameter import ParameterCreate
from fastapi import HTTPException

def fetch_all_parameters(db: Session):
    """ Service function to get all parameters. """
    parameters = get_all_parameters(db)
    if not parameters:
        raise HTTPException(status_code=404, detail="No parameters found")
    return parameters

def fetch_parameter_by_id(db: Session, parameter_id: int):
    """ Service function to get a parameter by ID. """
    parameter = get_parameter_by_id(db, parameter_id)
    if not parameter:
        raise HTTPException(status_code=404, detail=f"Parameter with ID {parameter_id} not found")
    return parameter

def create_parameter(db: Session, parameter_data: ParameterCreate):
    """ Service function to create a parameter with validation. """
    return add_parameter(db, parameter_data.dict())


#historical report

def get_parameter_id(db: Session, cycle_id: int, parameter_title: str):
    parameter = get_parameter_id_by_name(db, cycle_id, parameter_title)
    if not parameter:
        return None
    return parameter[0]  # Extracting parameter_id from tuple
