from pydantic import BaseModel, Field
from datetime import date
from typing import List

class LeadAssessmentRatingRequest(BaseModel):
    cycle_id: int
    employee_id: int
    ratings: List[dict]  # [{ "parameter_ID": int, "parameter_rating": int, "specific_input": str }]
    discussion_date: date

    class Config:
        orm_mode = True
