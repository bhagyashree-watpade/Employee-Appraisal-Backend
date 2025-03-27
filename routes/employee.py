from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional,List
from database.connection import get_db
from services.employee import get_all_employees
# , get_filtered_employees, get_selected_columns

router = APIRouter()

@router.get("/")
def read_employees_list(db:Session = Depends(get_db)):
    return get_all_employees(db)

# @router.get("/employees")
# def read_filtered_employees(
#     db:Session = Depends(get_db),
#     role: Optional[str] = None,
#     name: Optional[str] = None,
#     emp_id: Optional[int] = None,
#     manager: Optional[str] = None
# ):
#     return get_filtered_employees(db, role, name, emp_id, manager)

# @router.get("/employees")
# def read_selected_columns(db:Session = Depends(get_db), columns: Optional[List[str]] = None):
#     return get_selected_columns(db, columns)
