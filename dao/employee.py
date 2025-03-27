from sqlalchemy.orm import Session
from typing import Optional,List
from models.employee import Employee

def fetch_all_employees(db:Session):
    employees_list = db.query(Employee).all()
    return employees_list

