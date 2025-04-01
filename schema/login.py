from pydantic import BaseModel

class LoginRequest(BaseModel):
    employee_id: int
    password: str
