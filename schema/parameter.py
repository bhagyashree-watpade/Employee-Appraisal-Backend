from pydantic import BaseModel
# from datetime import date
# from typing import Optional

class ParameterBase(BaseModel):
    parameter_title: str
    helptext : str
    cycle_id: int
    applicable_to_employee : bool
    applicable_to_lead : bool
    is_fixed_parameter : bool

class ParameterCreate(ParameterBase):
    pass  # Used for creating a new stage

class ParameterResponse(ParameterBase):
    parameter_id: int

    class Config:
        orm_mode = True  # (For older FastAPI versions)

