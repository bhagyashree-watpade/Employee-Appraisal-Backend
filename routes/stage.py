from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.connection import get_db
from services.stage import fetch_all_stages, add_new_stage, fetch_self_assessment_stage_info, fetch_lead_assessment_stage_info
from schema.stage import StageCreate, StageResponse, StageInfoResponse
from typing import List

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


#route to get information about self assessment stage based on cycle id
@router.get("/self-assessment/{cycle_id}", response_model=StageInfoResponse)
def get_self_assessment_stage(cycle_id: int, db: Session = Depends(get_db)):
    return fetch_self_assessment_stage_info(cycle_id, db)


#route to get information about lead assessment stage based on cycle id
@router.get("/lead-assessment/{cycle_id}", response_model=StageInfoResponse)
def get_lead_assessment_stage(cycle_id: int, db: Session = Depends(get_db)):
    return fetch_lead_assessment_stage_info(cycle_id, db)
