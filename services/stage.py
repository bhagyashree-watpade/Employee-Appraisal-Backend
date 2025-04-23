from sqlalchemy.orm import Session
from dao.stage import get_all_stages, create_stage, get_self_assessment_stage_by_cycle_id, get_lead_assessment_stage_by_cycle_id
from schema.stage import StageCreate, StageInfoResponse
from fastapi import HTTPException

# Get all stages
def fetch_all_stages(db: Session):
    return get_all_stages(db)

# Add a new stage
def add_new_stage(db: Session, stage_data: StageCreate):
    return create_stage(db, stage_data)


def fetch_self_assessment_stage_info(cycle_id: int, db: Session) -> StageInfoResponse:
    stage = get_self_assessment_stage_by_cycle_id(db, cycle_id)
    if not stage:
        raise HTTPException(status_code=404, detail="Self Assessment stage not found for the given cycle ID")
    
    return StageInfoResponse(
        start_date_of_stage=stage.start_date_of_stage,
        end_date_of_stage=stage.end_date_of_stage,
        is_active=stage.is_active,
        is_completed=stage.is_completed
        
    )
    
def fetch_lead_assessment_stage_info(cycle_id: int, db: Session) -> StageInfoResponse:
    stage = get_lead_assessment_stage_by_cycle_id(db, cycle_id)
    if not stage:
        raise HTTPException(status_code=404, detail="Lead Assessment stage not found for the given cycle ID")
    
    return StageInfoResponse(
        start_date_of_stage=stage.start_date_of_stage,
        end_date_of_stage=stage.end_date_of_stage,
        is_active=stage.is_active,
        is_completed=stage.is_completed
        
    )