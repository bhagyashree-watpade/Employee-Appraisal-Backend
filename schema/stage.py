from pydantic import BaseModel
from datetime import date
# from typing import Optional

class StageBase(BaseModel):
    stage_name: str
    cycle_id: int
    start_date_of_stage: date
    end_date_of_stage: date

class StageCreate(StageBase):
    pass  # Used for creating a new stage

class StageResponse(StageBase):
    stage_id: int

    class Config:
        orm_mode = True  # Allows SQLAlchemy models to be converted to Pydantic models
