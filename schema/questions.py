from pydantic import BaseModel
from typing import List, Optional

class OptionSchema(BaseModel):
  option_text: str

class QuestionSchema(BaseModel):
  question_type: str
  question_text: str
  options: Optional[List[OptionSchema]] = []

  class Config:
    arbitrary_types_allowed = True

class QuestionResponseSchema(QuestionSchema):
  question_id: int
  options: List[OptionSchema]