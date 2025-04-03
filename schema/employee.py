from pydantic import BaseModel

class EmployeeListResponse(BaseModel):
    employee_id: int
    employee_name: str
    reporting_manager_name: str | None
