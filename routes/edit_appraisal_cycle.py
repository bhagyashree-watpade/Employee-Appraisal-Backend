from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.connection import get_db
from dao.edit_appraisal_cycle import get_cycle, edit_cycle
from sqlalchemy.exc import SQLAlchemyError
from models.edit_appraisal_cycle import CycleUpdate

router = APIRouter(tags=["Edit Appraisal Cycle"])


@router.get("/edit-appraisal-cycle/{cycle_id}")
def get_appraisal_cycle(cycle_id: int, db: Session = Depends(get_db)):
    """
    Get an appraisal cycle by its ID
    """
    try:
        cycle = get_cycle(db, cycle_id)
        return cycle
    except HTTPException as http_err:
        raise
    except SQLAlchemyError as db_err:
        raise HTTPException(status_code=500, detail="Database error while retrieving appraisal cycle")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error while retrieving appraisal cycle")



@router.put("/edit-appraisal-cycle/{cycle_id}")
def edit_appraisal_cycle(cycle_id: int, cycle_data: CycleUpdate, db: Session = Depends(get_db)):
    """
    Update an appraisal cycle by its ID
    """
    try:
        response = edit_cycle(db, cycle_id, cycle_data)
        return response
    except HTTPException as http_err:
        raise
    except ValueError as val_err:
        raise HTTPException(status_code=422, detail=str(val_err))
    except SQLAlchemyError as db_err:
        raise HTTPException(status_code=500, detail="Database error while updating appraisal cycle")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error while updating appraisal cycle")