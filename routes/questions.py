from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from database.connection import get_db
from sqlalchemy.orm import Session
from schema.questions import QuestionSchema, QuestionResponseSchema, QuestionsSchema
from typing import List
from dao.questions import get_all_questions, add_new_question, add_options, get_all_questions_with_option
router = APIRouter()


#get the list of question texts and ids for the questionnaire page
@router.get("/question", response_model=List[QuestionsSchema])
def list_question(db: Session = Depends(get_db)):
    questions = get_all_questions(db)
    # print("All questions fetched", questions)
    if not questions:
        raise HTTPException(status_code=404, detail="No questions found")
    return questions


#get the list of questions, with the options for the question allocation page
@router.get("/questions-with-options", response_model=List[QuestionResponseSchema])
def list_of_questions_with_options(db: Session = Depends(get_db)):
    questions = get_all_questions_with_option(db)
    # print("All questions fetched", questions)
    if not questions:
        raise HTTPException(status_code=404, detail="No questions found")
    return questions



@router.post("/question", response_model=QuestionResponseSchema)
def add_question(question_data: QuestionSchema, db: Session = Depends(get_db)):
    new_question = add_new_question(question_data, db)

    # Add options if applicable
    if question_data.question_type in ["MCQ", "Single Choice", "Yes/No"] and question_data.options:
        add_options(new_question.question_id, question_data.options, db)

    return JSONResponse(content={"message": "Question added successfully"}, status_code=201)