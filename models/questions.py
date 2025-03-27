from sqlalchemy import Column, Integer, String, Text, ForeignKey
from database.connection import Base
from sqlalchemy.orm import relationship


class Question(Base):
    __tablename__ = "question"

    question_id = Column(Integer, primary_key=True, autoincrement=True)
    question_text = Column(Text, nullable=False)  # Question text
    question_type = Column(String(50))
    options = relationship("Option", back_populates="question", cascade="all, delete-orphan")

class Option(Base):
    __tablename__ = "option"
    option_id = Column(Integer, primary_key=True, autoincrement=True)
    question_id = Column(Integer, ForeignKey("question.question_id", ondelete="CASCADE"))
    option_text = Column(Text, nullable=False)
    question = relationship("Question", back_populates="options")