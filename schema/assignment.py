from pydantic import BaseModel
from typing import List

# class AssignmentCreate(BaseModel):
#     employee_id: int
#     question_ids: List[int]
#     cycle_id: int

class AssignmentCreate(BaseModel):
    employee_ids: List[int]  # ✅ Changed to plural because it's now a list
    question_ids: List[int]
    cycle_id: int

class AssignmentResponse(BaseModel):
    employee_id: int
    cycle_id: int
    question_ids: List[int]  # Explicitly define question IDs in response

    class Config:
        from_attributes = True  # Ensures conversion from SQLAlchemy models