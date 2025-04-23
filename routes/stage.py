from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database.connection import get_db
from services.stage import fetch_all_stages, add_new_stage
from schema.stage import StageCreate, StageResponse
from typing import List
from models import Stage
from models import AppraisalCycle

router = APIRouter(prefix="/stages", tags=["Stages"])

# Fetch all stages
@router.get("/", response_model=List[StageResponse])
def get_stages(db: Session = Depends(get_db)):
    stages = fetch_all_stages(db)
    if not stages:
        raise HTTPException(status_code=404, detail="No stages found")
    return stages

# Add a new stage with validation
@router.post("/", response_model=StageResponse)
def create_new_stage(stage_data: StageCreate, db: Session = Depends(get_db)):
    return add_new_stage(db, stage_data)




# To update stage automatically
# @router.get("/current", response_model=StageResponse)
# def get_current_stage(
#     cycle_id: int = Query(..., description="Cycle ID to get the current stage for"),
#     db: Session = Depends(get_db)
# ):
#     current_stage = db.query(Stage).filter(
#         Stage.cycle_id == cycle_id,
#         Stage.is_active == True
#     ).first()

#     if not current_stage:
#         raise HTTPException(status_code=404, detail="No active stage found for the given cycle")

#     return current_stage    




@router.get("/current", response_model=StageResponse)
def get_current_stage(
    cycle_id: int = Query(..., description="Cycle ID to get the current stage for"),
    db: Session = Depends(get_db)
):
    # Fetch the cycle
    cycle = db.query(AppraisalCycle).filter(AppraisalCycle.cycle_id == cycle_id).first()
    if not cycle:
        raise HTTPException(status_code=404, detail="Cycle not found")

    # If cycle is inactive, return the "Setup" stage
    if cycle.status == "inactive":
        setup_stage = db.query(Stage).filter(
            Stage.cycle_id == cycle_id,
            Stage.stage_name.ilike("Setup")  # case-insensitive match
        ).first()

        if not setup_stage:
            raise HTTPException(status_code=404, detail="Setup stage not found for inactive cycle")
        
        return setup_stage

    # For active cycles, return the active stage
    current_stage = db.query(Stage).filter(
        Stage.cycle_id == cycle_id,
        Stage.is_active == True
    ).first()

    if not current_stage:
        raise HTTPException(status_code=404, detail="No active stage found for the given cycle")

    return current_stage

