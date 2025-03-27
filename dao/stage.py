
from sqlalchemy.orm import Session
from models.stages import Stage
from models.appraisal_cycle import AppraisalCycle
from schema.stage import StageCreate
from fastapi import HTTPException

# Fetch all stages
def get_all_stages(db: Session):
    return db.query(Stage).all()

# Check if cycle_id exists
def get_cycle_by_id(db: Session, cycle_id: int):
    return db.query(AppraisalCycle).filter(AppraisalCycle.cycle_id == cycle_id).first()

# Create a new stage with validation
def create_stage(db: Session, stage_data: StageCreate):
    cycle = get_cycle_by_id(db, stage_data.cycle_id)
    
    if not cycle:
        raise HTTPException(status_code=404, detail=f"Appraisal Cycle with ID {stage_data.cycle_id} not found")

    # Validate if stage dates are within cycle dates
    if not (cycle.start_date_of_cycle <= stage_data.start_date_of_stage <= cycle.end_date_of_cycle):
        raise HTTPException(status_code=400, detail="Stage start date must be within the cycle start and end dates")
    
    if not (cycle.start_date_of_cycle <= stage_data.end_date_of_stage <= cycle.end_date_of_cycle):
        raise HTTPException(status_code=400, detail="Stage end date must be within the cycle start and end dates")
    
    if stage_data.start_date_of_stage > stage_data.end_date_of_stage:
        raise HTTPException(status_code=400, detail="Stage start date cannot be after end date")

    new_stage = Stage(**stage_data.dict())
    db.add(new_stage)
    db.commit()
    db.refresh(new_stage)
    return new_stage
