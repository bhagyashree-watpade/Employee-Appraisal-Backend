

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.connection import get_db
from services.parameter import fetch_all_parameters, fetch_parameter_by_id, create_parameter
from schema.parameter import ParameterCreate, ParameterResponse
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
