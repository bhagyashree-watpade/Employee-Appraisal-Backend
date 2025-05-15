from sqlalchemy.orm import Session
from dao.employee import get_employee_by_id, get_employee_by_role_id
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status

def authenticate_employee(db: Session, employee_id: int, password: str):
    """Authenticate employee by checking if the provided password matches the stored one."""
    try:
        # Try to fetch the employee based on role ID (for this specific case)
        employee = get_employee_by_role_id(db, employee_id)

        # If no employee found, return None
        if not employee:
            return None  # Employee not found

        # If password mismatch, return None
        if employee.password != password:
            return None  # Password mismatch

        # Successful authentication
        return employee

    except SQLAlchemyError as exception:
        # Handle database-related exceptions (connection issues)
        print(f"Database error occurred: {exception}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred"
        )
        # return None

    except Exception as e:
        # Catch any other unexpected errors
        print(f"Unexpected error: {e}")
        # return None
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )