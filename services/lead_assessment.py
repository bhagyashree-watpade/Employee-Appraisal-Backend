from sqlalchemy.orm import Session
from dao.lead_assessment import get_overall_performance_rating, save_lead_assessment_rating
from fastapi import HTTPException


def save_lead_assessment_rating_service(db: Session, cycle_id: int, employee_id: int, ratings: list, discussion_date):
    try:
        result = save_lead_assessment_rating(
            db=db,
            cycle_id=cycle_id,
            employee_id=employee_id,
            ratings=ratings,
            discussion_date=discussion_date
        )
        return result
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception:
        # raise e
        raise HTTPException(status_code=500, detail="Internal server error")


#historical report


def get_overall_rating_of_employee(db: Session, cycle_id: int):
    return get_overall_performance_rating(db, cycle_id)
