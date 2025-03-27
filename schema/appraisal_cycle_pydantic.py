from pydantic import BaseModel
from datetime import date
from typing import Literal

class AppraisalCycleCreate(BaseModel):
    cycle_name: str
    description: str
    status: Literal["active", "inactive"]  # Restricts status to these values
    start_date_of_cycle: date
    end_date_of_cycle: date

class AppraisalCycleResponse(AppraisalCycleCreate):
    cycle_id: int  # Include ID in the response

    class Config:
        from_attributes = True  # Allows SQLAlchemy models to be converted into Pydantic models
