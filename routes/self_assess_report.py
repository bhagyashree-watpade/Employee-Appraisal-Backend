from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.connection import get_db
from dao.temp_self_assess_repo import get_response
from schema.edit_appraisal_cycle import GetAppraisalCycleResponse
import logging
from models.appraisal_cycle import AppraisalCycle
from logger_config import logging

router = APIRouter(prefix="/self-assessment-report", tags=["Self Assessment Report Temp"])

@router.get("/{cycle_id}")
def get_active_cycle( cycle_id:int,db: Session = Depends(get_db)):
  logging.info("Incoming request to get /self-assessment-report endpoint by user.")
  responses = get_response(db,cycle_id)
  if not responses:
    logging.error("No responses found in the database.")
    raise HTTPException(status_code=404, detail="No responses found")
  logging.info(f"Fetched 1 cycle successfully.")
  return responses
