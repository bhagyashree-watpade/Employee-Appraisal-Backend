from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.connection import get_db
from dao.edit_appraisal_cycle import get_cycle, edit_cycle
# update_appraisal_cycle
from schema.edit_appraisal_cycle import GetAppraisalCycleResponse
import logging
from models.edit_appraisal_cycle import CycleUpdate
from logger_config import logging

router = APIRouter(prefix="/edit-appraisal-cycle", tags=["Edit Appraisal Cycle"])

@router.get("/{cycle_id}")
def get_appraisal_cycle(cycle_id:int, db: Session = Depends(get_db)):
  logging.info("Incoming request to /edit-appraisal-cycle endpoint by user.")
  cycle = get_cycle(db, cycle_id)
  if not cycle:
    logging.error("No cycle found in the database.")
    raise HTTPException(status_code=404, detail="No cycle found")
  logging.info(f"Fetched 1 cycle successfully.")
  return cycle

@router.put("/{cycle_id}")
def edit_appraisal_cycle(cycle_id:int, cycle_data:CycleUpdate, db: Session = Depends(get_db)):
  logging.info("Incoming request to /edit-appraisal-cycle endpoint by user.")
  logging.info("Received request to update appraisal cycle: %s",cycle_data.cycle_name)
  update_message = edit_cycle(db,cycle_id,cycle_data)
  logging.info(f"Cycle with ID {cycle_id} updated successfully.")
  return {"message":update_message}
  