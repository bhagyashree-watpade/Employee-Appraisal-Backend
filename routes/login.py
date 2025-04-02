from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schema.login import LoginRequest
from services.login import authenticate_employee
from database.connection import get_db

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    employee = authenticate_employee(db, request.employee_id, request.password)
    if not employee:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    return {"message": "Login successful", "employee_id": employee.employee_id, "role": employee.role}
