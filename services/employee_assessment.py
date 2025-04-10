from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import List
from collections import defaultdict
from schema.employee_assessment import AssessmentResponseIn, AssessmentResponseOut
from models.self_assessment_response import SelfAssessmentResponse
from models.questions import Option
from dao.employee_assessment import get_allocated_cycles,get_assigned_questions_with_options,get_existing_responses,submit_self_assessment_responses,get_cycle_status


def get_employee_cycles(db: Session, employee_id: int):
    return get_allocated_cycles(db, employee_id)

def get_questions_for_cycle(db: Session, employee_id: int, cycle_id: int):
    questions = get_assigned_questions_with_options(db, employee_id, cycle_id)
    return questions

def save_self_assessment_responses(db: Session, responses: List[AssessmentResponseIn]):
    if not responses:
        return {"message": "No responses submitted."}

    cycle_status = get_cycle_status(db, responses[0].cycle_id)
    if not cycle_status:
        raise ValueError("Invalid cycle_id.")

    if cycle_status == "completed":
        raise HTTPException(status_code=403, detail="Responses cannot be submitted for completed cycle.")

    # Delete old responses for the same question+employee
    for res in responses:
        db.query(SelfAssessmentResponse).filter(
            SelfAssessmentResponse.employee_id == res.employee_id,
            SelfAssessmentResponse.cycle_id == res.cycle_id,
            SelfAssessmentResponse.question_id == res.question_id
        ).delete()

    # Add updated responses
    response_objs = []
    for res in responses:
        if res.option_ids:  # Multiple option selection
            for oid in res.option_ids:
                option = db.query(Option).filter_by(option_id=oid).first()
                response_objs.append(
                    SelfAssessmentResponse(
                        allocation_id=res.allocation_id,
                        employee_id=res.employee_id,
                        cycle_id=res.cycle_id,
                        question_id=res.question_id,
                        option_id=oid,
                        response_text=option.option_text if option else None  # 🟢 Save readable text too
                    )
                )


        else:
            # Descriptive or single option text
            if res.response_text:
                for text in res.response_text:
                    response_objs.append(
                        SelfAssessmentResponse(
                            allocation_id=res.allocation_id,
                            employee_id=res.employee_id,
                            cycle_id=res.cycle_id,
                            question_id=res.question_id,
                            option_id=None,
                            response_text=text
                        )
                    )

    submit_self_assessment_responses(db, response_objs)
    return {"message": "Responses updated successfully"}



def get_readonly_responses(db: Session, employee_id: int, cycle_id: int) -> List[AssessmentResponseOut]:
    raw_responses = get_existing_responses(db, employee_id, cycle_id)

    grouped = defaultdict(list)

    # Group by question
    for res in raw_responses:
        grouped[res.question_id].append(res)

    formatted_responses = []

    for question_id, responses in grouped.items():
        first = responses[0]  # same question info for all

        option_ids = []
        response_texts = set()


        for res in responses:
            if res.option:
                option_ids.append(res.option.option_id)
                response_texts.add(res.option.option_text)
            if res.response_text:
                response_texts.add(res.response_text)

        formatted_responses.append(
            AssessmentResponseOut(
                question_id=first.question.question_id,
                question_text=first.question.question_text,
                question_type=first.question.question_type,
                option_ids=option_ids if option_ids else None,
                response_text=list(response_texts) if response_texts else None
            )
        )

    return formatted_responses

