
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schema.lead_assessment import LeadAssessmentRatingRequest,LeadAssessmentRatingResponse
from services.lead_assessment import save_lead_assessment_rating, get_overall_rating_of_employee
from models.lead_assessment import LeadAssessmentRating
from models.appraisal_cycle import   AppraisalCycle
from database.connection import get_db

router = APIRouter(prefix="/lead_assessment", tags=["Lead Assessment"])

@router.post("/save_rating")
def save_rating(request: LeadAssessmentRatingRequest, db: Session = Depends(get_db)):
    try:
        # Check if the cycle is active
        cycle = db.query(AppraisalCycle).filter(AppraisalCycle.cycle_id == request.cycle_id).first()
        if not cycle:
            raise HTTPException(status_code=404, detail="Appraisal cycle not found")

        if cycle.status.lower() != "active":
            raise HTTPException(status_code=400, detail="The selected appraisal cycle is not active.")

        result = save_lead_assessment_rating(
            db,
            cycle_id=request.cycle_id,
            employee_id=request.employee_id,
            ratings=request.ratings,
            discussion_date=request.discussion_date
        )
        return result
    except ValueError as ve:
        # Handle case when allocation is not found
        if "No allocation found" in str(ve):  
            raise HTTPException(status_code=404, detail="No allocation found for the selected cycle and employee.")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error.")



@router.get("/lead_assessment/previous_data/{cycle_id}/{employee_id}")
def get_previous_ratings(cycle_id: int, employee_id: int, db: Session = Depends(get_db)):
    # Fetch cycle status
    cycle = db.query(AppraisalCycle).filter(AppraisalCycle.cycle_id == cycle_id).first()
    if not cycle:
        raise HTTPException(status_code=404, detail="Appraisal cycle not found")

    # Fetch previous ratings for the given employee and cycle
    previous_ratings = db.query(LeadAssessmentRating).filter(
        LeadAssessmentRating.cycle_id == cycle_id,
        LeadAssessmentRating.employee_id == employee_id
    ).all()

    return {
        "cycle_status": cycle.status,  # Include cycle status in the response
        "ratings": [{"parameter_id": r.parameter_id, "parameter_rating": r.parameter_rating, "specific_input": r.specific_input} for r in previous_ratings],
        "discussion_date": previous_ratings[0].discussion_date if previous_ratings else None
    }


#historic report

#for getting list of employee_id and "overall performance rating" for a selected cycle
@router.get("/employees_ratings/{cycle_id}", response_model=list[LeadAssessmentRatingResponse])
def get_employee_ratings(cycle_id: int, db: Session = Depends(get_db)):
    data =get_overall_rating_of_employee(db, cycle_id)
    if not data:
        raise HTTPException(status_code=404, detail="No data found for this cycle or parameter.")
    return data