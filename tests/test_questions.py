# from fastapi.testclient import TestClient
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import app

# client = TestClient(app)



# def test_add_descriptive_question():
#     payload = {
#         "question_type": "Descriptive",
#         "question_text": "Do you live movies?",
#         "options": None
#     }
#     response = client.post("/question", json=payload)
#     assert response.status_code == 201
#     assert response.json() == {"message": "Question added successfully"}

# def test_add_mcq_question():
#   payload = {
#     "question_type":"MCQ",
#     "question_text":"Which is your favorite team?",
#     "options":[{"option_text": "MI"},{"option_text": "CSK"},{"option_text": "KKR"}]
#   }
#   response = client.post("/question", json=payload)
#   assert response.status_code == 201
#   assert response.json() == {"message": "Question added successfully"}

# def test_yes_no_question():
#   payload = {
#     "question_type":"Yes/No",
#     "question_text":"Do you like testing?",
#     "options":[{"option_text":"Yes"},{"option_text":"No"}]
#   }
#   response = client.post("/question",json=payload)
#   assert response.status_code == 201
#   assert response.json() == {"message": "Question added successfully"}

# def test_get_all_questions():
#   response = client.get("/question") 
#   assert response.status_code == 200


import pytest
from fastapi.testclient import TestClient
from fastapi import status
from unittest.mock import MagicMock, patch
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from models.questions import Question, Option
from schema.questions import QuestionSchema
from dao.questions import (
    get_all_questions, 
    add_new_question, 
    add_options, 
    get_all_questions_with_option
)
from main import app  # Import your FastAPI instance

# Create a test client
client = TestClient(app)

# Mock data for testing
mock_question_list = [
    MagicMock(question_id=86, question_text="Do you have a plan for your personal development?"),
    MagicMock(question_id=87, question_text="Have you led a team or a project?")
]

# [{
#     "question_id": 86,
#     "question_text": "Do you have a plan for your personal development?"
#   },
#   {
#     "question_id": 87,
#     "question_text": "Have you led a team or a project?"
#   }]

mock_questions_with_options = [
    MagicMock(
        question_id=1,
        question_text="What is your favorite color?",
        question_type="MCQ",
        options=[
            MagicMock(option_id=1, option_text="Red", question_id=1),
            MagicMock(option_id=2, option_text="Blue", question_id=1),
        ]
    ),
    MagicMock(
        question_id=2,
        question_text="Are you a student?",
        question_type="Yes/No",
        options=[
            MagicMock(option_id=3, option_text="Yes", question_id=2),
            MagicMock(option_id=4, option_text="No", question_id=2),
        ]
    )
]

mock_question_schema = QuestionSchema(
    question_type="MCQ",
    question_text="What is your favorite food?",
    options=[{"option_text":"Pizza"}, {"option_text":"Burger"}]
)

# Test DAO functions
class TestQuestionDAO:
    @patch('dao.questions.Session')
    def test_get_all_questions_success(self, mock_db):
        # Arrange
        mock_db.query().all.return_value = mock_question_list
        
        # Act
        result = get_all_questions(mock_db)
        
        # Assert
        assert result == mock_question_list
        mock_db.query.assert_called_once()
    
    @patch('dao.questions.Session')
    def test_get_all_questions_db_error(self, mock_db):
        # Arrange
        mock_db.query.side_effect = SQLAlchemyError("Database error")
        
        # Act & Assert
        with pytest.raises(SQLAlchemyError):
            get_all_questions(mock_db)
    
    @patch('dao.questions.Session')
    def test_get_all_questions_with_option_success(self, mock_db):
        # Arrange
        mock_query = MagicMock()
        mock_db.query.return_value = mock_query
        mock_query.options.return_value.all.return_value = mock_questions_with_options
        
        # Act
        result = get_all_questions_with_option(mock_db)
        
        # Assert
        assert result == mock_questions_with_options
        mock_db.query.assert_called_once()
        mock_query.options.assert_called_once()
    
    @patch('dao.questions.Session')
    def test_get_all_questions_with_option_db_error(self, mock_db):
        # Arrange
        mock_db.query.side_effect = SQLAlchemyError("Database error")
        
        # Act & Assert
        with pytest.raises(SQLAlchemyError):
            get_all_questions_with_option(mock_db)
    
    @patch('dao.questions.Session')
    def test_add_new_question_success(self, mock_db):
        # Arrange
        mock_question = MagicMock(question_id=3)
        mock_db.add.return_value = None
        mock_db.commit.return_value = None
        mock_db.refresh = MagicMock(side_effect=lambda x: setattr(x, 'question_id', 3))
        
        # Act
        result = add_new_question(mock_question_schema, mock_db)
        
        # Assert
        assert result.question_id == 3
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once()
    
    @patch('dao.questions.Session')
    def test_add_new_question_integrity_error(self, mock_db):
        # Arrange
        mock_db.add.return_value = None
        mock_db.commit.side_effect = IntegrityError("Integrity violation", None, None)
        
        # Act & Assert
        with pytest.raises(IntegrityError):
            add_new_question(mock_question_schema, mock_db)
        mock_db.rollback.assert_called_once()
    
    @patch('dao.questions.Session')
    def test_add_options_success(self, mock_db):
        # Arrange
        options = ["Option 1", "Option 2"]
        mock_db.add_all.return_value = None
        mock_db.commit.return_value = None
        
        # Act
        result = add_options(1, options, mock_db)
        
        # Assert
        assert len(result) == 2
        assert result[0].option_text == "Option 1"
        assert result[1].option_text == "Option 2"
        mock_db.add_all.assert_called_once()
        mock_db.commit.assert_called_once()
    
    @patch('dao.questions.Session')
    def test_add_options_db_error(self, mock_db):
        # Arrange
        options = ["Option 1", "Option 2"]
        mock_db.add_all.return_value = None
        mock_db.commit.side_effect = SQLAlchemyError("Database error")
        
        # Act & Assert
        with pytest.raises(SQLAlchemyError):
            add_options(1, options, mock_db)
        mock_db.rollback.assert_called_once()

# Test API Routes
class TestQuestionRoutes:
    @patch('routes.questions.get_all_questions')
    def test_list_question_success(self, mock_get_all_questions):
        # Arrange
        mock_get_all_questions.return_value = mock_question_list
        
        # Act
        response = client.get("/question")
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 2
        mock_get_all_questions.assert_called_once()
    
    @patch('routes.questions.get_all_questions')
    def test_list_question_empty(self, mock_get_all_questions):
        # Arrange
        mock_get_all_questions.return_value = []
        
        # Act
        response = client.get("/question")
        
        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"detail": "No questions found"}
        mock_get_all_questions.assert_called_once()
    
    @patch('routes.questions.get_all_questions')
    def test_list_question_db_error(self, mock_get_all_questions):
        # Arrange
        mock_get_all_questions.side_effect = SQLAlchemyError("Database error")
        
        # Act
        response = client.get("/question")
        
        # Assert
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert "Failed to retrieve" in response.json()["detail"]
        mock_get_all_questions.assert_called_once()
    
    @patch('routes.questions.get_all_questions_with_option')
    def test_list_of_questions_with_options_success(self, mock_get_all_questions_with_option):
        # Arrange
        mock_get_all_questions_with_option.return_value = mock_questions_with_options
        
        # Act
        response = client.get("/questions-with-options")
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 2
        mock_get_all_questions_with_option.assert_called_once()
    
    @patch('routes.questions.get_all_questions_with_option')
    def test_list_of_questions_with_options_empty(self, mock_get_all_questions_with_option):
        # Arrange
        mock_get_all_questions_with_option.return_value = []
        
        # Act
        response = client.get("/questions-with-options")
        
        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"detail": "No questions found"}
        mock_get_all_questions_with_option.assert_called_once()
    
    @patch('routes.questions.get_all_questions_with_option')
    def test_list_of_questions_with_options_db_error(self, mock_get_all_questions_with_option):
        # Arrange
        mock_get_all_questions_with_option.side_effect = SQLAlchemyError("Database error")
        
        # Act
        response = client.get("/questions-with-options")
        
        # Assert
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert "Failed to retrieve" in response.json()["detail"]
        mock_get_all_questions_with_option.assert_called_once()
    
    @patch('routes.questions.add_options')
    @patch('routes.questions.add_new_question')
    def test_add_question_success(self, mock_add_new_question, mock_add_options):
        # Arrange
        mock_question = MagicMock(question_id=3)
        mock_add_new_question.return_value = mock_question
        
        # Act
        response = client.post(
            "/question",
            json={
                "question_type": "MCQ",
                "question_text": "What is your favorite food?",
                "options": ["Pizza", "Burger"]
            }
        )
        
        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        assert "Question added successfully" in response.json()["message"]
        mock_add_new_question.assert_called_once()
        mock_add_options.assert_called_once()
    
    def test_add_question_missing_options(self):
        # Act
        response = client.post(
            "/question",
            json={
                "question_type": "MCQ",
                "question_text": "What is your favorite food?",
                "options": []
            }
        )
        
        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "require at least one option" in response.json()["detail"]
    
    def test_add_question_missing_required_fields(self):
        # Act
        response = client.post(
            "/question",
            json={
                "question_type": "",
                "question_text": "What is your favorite food?",
                "options": ["Pizza", "Burger"]
            }
        )
        
        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "required" in response.json()["detail"]
    
    @patch('routes.questions.add_new_question')
    def test_add_question_db_error(self, mock_add_new_question):
        # Arrange
        mock_add_new_question.side_effect = SQLAlchemyError("Database error")
        
        # Act
        response = client.post(
            "/question",
            json={
                "question_type": "MCQ",
                "question_text": "What is your favorite food?",
                "options": ["Pizza", "Burger"]
            }
        )
        
        # Assert
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert "Failed to add question" in response.json()["detail"]
        mock_add_new_question.assert_called_once()
    
    @patch('routes.questions.add_new_question')
    def test_add_question_integrity_error(self, mock_add_new_question):
        # Arrange
        mock_add_new_question.side_effect = IntegrityError("Integrity error", None, None)
        
        # Act
        response = client.post(
            "/question",
            json={
                "question_type": "MCQ",
                "question_text": "What is your favorite food?",
                "options": ["Pizza", "Burger"]
            }
        )
        
        # Assert
        assert response.status_code == status.HTTP_409_CONFLICT
        assert "conflict" in response.json()["detail"]
        mock_add_new_question.assert_called_once()