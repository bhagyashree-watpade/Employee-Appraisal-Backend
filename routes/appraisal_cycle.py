
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from services.appraisal_cycle import add_new_cycle, fetch_all_cycles, fetch_cycle_by_id, fetch_all_cycles_with_stages, delete_appraisal_cycle
from schema.appraisal_cycle_pydantic import AppraisalCycleCreate, AppraisalCycleResponse, AppraisalCycleResponseWithStages
from database.connection import get_db
from models.appraisal_cycle import AppraisalCycle  # Import your AppraisalCycle model
import logging
from logger_config import logging
router = APIRouter(prefix="/appraisal_cycle", tags=["Appraisal Cycle"])

# Create a new cycle
@router.post("/", response_model=AppraisalCycleResponse)
def create_cycle(cycle_data: AppraisalCycleCreate, db: Session = Depends(get_db)):
    if cycle_data.status not in ["active", "inactive"]:
        raise HTTPException(status_code=400, detail="Invalid status. Allowed values: 'active', 'inactive'")
    return add_new_cycle(db, cycle_data)

# Get all cycles
@router.get("/", response_model=list[AppraisalCycleResponse])
def get_cycles(db: Session = Depends(get_db)):
    return fetch_all_cycles(db)

# Get all cycles with stage names
@router.get("/with-stage-names", response_model=list[AppraisalCycleResponseWithStages])
def get_cycles_with_stage_names(db: Session = Depends(get_db)):
    logging.info("Fetching appraisal cycles with stage names")
    result = fetch_all_cycles_with_stages(db)
    logging.info("Fetched %d appraisal cycles", len(result))
    return result

# Get cycle by ID
@router.get("/{cycle_id}", response_model=AppraisalCycleResponse)
def get_cycle(cycle_id: int, db: Session = Depends(get_db)):
    cycle = fetch_cycle_by_id(db, cycle_id)
    if not cycle:
        raise HTTPException(status_code=404, detail="Cycle not found")
    return cycle

# Delete cycle by ID
@router.delete("/{cycle_id}")
def delete_cycle(cycle_id: int, db: Session = Depends(get_db)):
    logging.info(f"Request to delete appraisal cycle with ID: {cycle_id}")
    result = delete_appraisal_cycle(db, cycle_id)
    logging.info(f"Appraisal cycle with ID {cycle_id} deleted successfully")
    return result

@router.get("/status/{cycle_id}")
def get_appraisal_cycle_status(cycle_id: int, db: Session = Depends(get_db)):
    """Fetch the status of an appraisal cycle by cycle_id."""
    cycle = db.query(AppraisalCycle).filter(AppraisalCycle.cycle_id == cycle_id).first()
    
    if not cycle:
        raise HTTPException(status_code=404, detail="Appraisal cycle not found")

    return {"cycle_id": cycle.cycle_id, "status": cycle.status}  # Assuming cycle has a 'status' field
