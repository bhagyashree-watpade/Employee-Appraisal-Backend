from sqlalchemy.orm import Session
from typing import Optional, List
from dao.employee import fetch_all_employees,get_all_employees_sorted
# filter_employees, fetch_columns

def get_all_employees(db:Session):
    return fetch_all_employees(db)
    
#for historical report
def get_sorted_employees(db: Session):
    return get_all_employees_sorted(db)