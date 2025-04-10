from sqlalchemy.orm import Session
from sqlalchemy import select, func, literal
from sqlalchemy.orm import aliased
from models.self_assessment_response import SelfAssessmentResponse
from models.questions import Question
from models.employee import Employee
from models.employee_allocation import EmployeeAllocation
from typing import List 

def get_response(db:Session, cycle_id:int):
  QuestionAlias = aliased(Question)
    
  subquery_questions = (
        db.query(SelfAssessmentResponse.question_id)
        .filter(SelfAssessmentResponse.cycle_id == cycle_id)
        .distinct()
        .subquery()
    )

  cross_joined = (
        db.query(EmployeeAllocation.employee_id, subquery_questions.c.question_id)
        .filter(EmployeeAllocation.cycle_id == cycle_id)
        .join(Employee, Employee.employee_id == EmployeeAllocation.employee_id)
        .join(subquery_questions, literal(True))  # cross join
        .subquery()
    )

  result = (
        db.query(
            Employee.employee_id,
            Employee.employee_name,
            Question.question_text,
            func.coalesce(SelfAssessmentResponse.response_text, literal('-')).label('response_text')
        )
        .select_from(cross_joined)
        .join(Employee, Employee.employee_id == cross_joined.c.employee_id)
        .join(Question, Question.question_id == cross_joined.c.question_id)
        .outerjoin(
            SelfAssessmentResponse,
            (SelfAssessmentResponse.employee_id == cross_joined.c.employee_id) &
            (SelfAssessmentResponse.question_id == cross_joined.c.question_id) &
            (SelfAssessmentResponse.cycle_id == cycle_id)
        )
        .order_by(Employee.employee_id, Question.question_id)
    )

  response = [
        {
            "employee_id": row.employee_id,
            "employee_name": row.employee_name,
            "question_text": row.question_text,
            "response_text": row.response_text
        }
        for row in result.all()
    ]

  return response