from sqlalchemy.orm import Session
from dao.stage import get_all_stages, create_stage
from schema.stage import StageCreate

# Get all stages
def fetch_all_stages(db: Session):
    return get_all_stages(db)

# Add a new stage
def add_new_stage(db: Session, stage_data: StageCreate):
    return create_stage(db, stage_data)
