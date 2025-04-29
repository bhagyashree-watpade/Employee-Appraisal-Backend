from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database.connection import get_db
from schema.employee_assessment import AssessmentResponseIn, AssessmentResponseOut,QuestionOut
from services.employee_assessment import (
    get_employee_cycles,
    get_questions_for_cycle,
    save_self_assessment_responses,
    get_readonly_responses
)
from dao.employee_assessment import get_team_lead_cycles

router = APIRouter(prefix="/assessment", tags=["Self Assessment"])

# Fetch the active(for which self assessment stage is either active or completed) and completed cycles for which employee is allocated
@router.get("/cycles/{employee_id}")
def fetch_employee_cycles(employee_id: int, db: Session = Depends(get_db)):
    cycles = get_employee_cycles(db, employee_id)
    if not cycles:
        raise HTTPException(status_code=404, detail="No appraisal cycles found for employee.")
    return cycles

# Fetch the active (for which self assessment stage is either active or completed)  and completed cycles  for which either the team lead or one of the employee under him is allocated 
@router.get("/teamlead/cycles/{team_lead_id}")
def fetch_team_lead_cycles(team_lead_id: int, db: Session = Depends(get_db)):
    cycles = get_team_lead_cycles(db, team_lead_id)
    if not cycles:
        raise HTTPException(status_code=404, detail="No appraisal cycles found for team lead.")
    return cycles

# Fetch questions assigned to the employee for active and completed cycles
@router.get("/questions/{employee_id}/{cycle_id}", response_model=List[QuestionOut])
def fetch_questions(employee_id: int, cycle_id: int, db: Session = Depends(get_db)):
    questions = get_questions_for_cycle(db, employee_id, cycle_id)
    if not questions:
        raise HTTPException(status_code=404, detail="No questions found.")
    return questions

# Add response and submit
@router.post("/submit", response_model=dict)
def submit_assessment(responses: List[AssessmentResponseIn], db: Session = Depends(get_db)):
    if not responses:
        raise HTTPException(status_code=400, detail="No responses submitted.")
    return save_self_assessment_responses(db, responses)

#  Fetch the responses 
@router.get("/responses/{employee_id}/{cycle_id}", response_model=List[AssessmentResponseOut])
def view_responses(employee_id: int, cycle_id: int, db: Session = Depends(get_db)):
    responses = get_readonly_responses(db, employee_id, cycle_id)
    if not responses:
        raise HTTPException(status_code=404, detail="No responses found.")
    return responses
