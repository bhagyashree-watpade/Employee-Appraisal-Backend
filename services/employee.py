from sqlalchemy.orm import Session
from typing import Optional, List
from dao.employee import fetch_all_employees
# filter_employees, fetch_columns

def get_all_employees(db:Session):
    return fetch_all_employees(db)
    
# def get_filtered_employees(
#         db:Session, 
#         role: Optional[str] = None, 
#         name: Optional[str] = None, 
#         emp_id: Optional[int] = None, 
#         manager: Optional[str] = None
# ):
#     return filter_employees(db, role, name, emp_id, manager)

# def get_selected_columns(db:Session, columns: Optional[List[str]] = None):
#     return fetch_columns(db, columns)