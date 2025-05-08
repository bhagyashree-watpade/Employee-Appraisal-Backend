from sqlalchemy.orm import Session, selectinload
from models.questions import Question, Option
from schema.questions import QuestionSchema
from typing import List


def get_all_questions(db: Session) -> List[Question]:
    #Fetch all questions from the database
    # print("All questions fetched", db.query(Question).all())
    # return db.query(Question).all()
    return db.query(Question.question_id, Question.question_text).all()


def get_all_questions_with_option(db: Session) -> List[Question]:
    #Fetch all questions with their options from the database
   return db.query(Question).options(selectinload(Question.options)).all()

def add_new_question(question_data: QuestionSchema, db: Session) -> Question:
    #Add a new question to the database
    new_question = Question(
        question_type=question_data.question_type,
        question_text=question_data.question_text
    )
    db.add(new_question)
    db.commit()
    db.refresh(new_question)
    return new_question

def add_options(question_id: int, options: List[str], db: Session):
    #Add options for MCQ, Single Choice, or Yes/No questions
    option_objects = [Option(question_id=question_id, option_text=opt.option_text) for opt in options]
    db.add_all(option_objects)
    db.commit()