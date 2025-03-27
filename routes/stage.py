from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.connection import get_db
from services.stage import fetch_all_stages, add_new_stage
from schema.stage import StageCreate, StageResponse
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
