from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from database.connection import get_db
from dao.temp_self_assess_repo import get_response
from models.appraisal_cycle import AppraisalCycle

router = APIRouter(tags=["Self Assessment Report"])

@router.get("/self-assessment-report/{cycle_id}")
def get_active_cycle(
    cycle_id: int, 
    db: Session = Depends(get_db)
):
    """
    Retrieve self-assessment responses for a specific cycle
    
    """
    try:
        cycle = db.query(AppraisalCycle).filter(AppraisalCycle.cycle_id == cycle_id).first()
        if not cycle:
            raise HTTPException(status_code=404, detail=f"Appraisal cycle with ID {cycle_id} not found")

        responses = get_response(db, cycle_id)
        
        if not responses:
            raise HTTPException(status_code=404, detail=f"No self-assessment responses found for cycle {cycle_id}")
        
        return responses
    
    except HTTPException:
        raise
    except SQLAlchemyError as db_err:
        raise HTTPException(status_code=500, detail="Database error while retrieving self-assessment report")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error while retrieving self-assessment report")