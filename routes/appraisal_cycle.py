
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from services.appraisal_cycle import add_new_cycle, fetch_all_cycles, fetch_cycle_by_id, fetch_all_cycles_with_stages, delete_appraisal_cycle
from schema.appraisal_cycle_pydantic import AppraisalCycleCreate, AppraisalCycleResponse, AppraisalCycleResponseWithStages
from database.connection import get_db

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
    return fetch_all_cycles_with_stages(db)

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
    return delete_appraisal_cycle(db,cycle_id)


