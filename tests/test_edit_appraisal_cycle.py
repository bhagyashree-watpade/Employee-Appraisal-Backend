# from fastapi.testclient import TestClient
import sys 
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# from main import app

# client = TestClient(app)

# def test_get_appraisal_cycle():
#   cycle_id = 102
#   response = client.get(f"/edit-appraisal-cycle/{cycle_id}")
#   assert response.status_code == 200 or response.status_code == 404
  
# def test_edit_appraisal_cycle():
#   cycle_id = 109
#   payload = {
#     "cycle_name": "Edit pytest",
#     "description": "Edit",
#     "status": "inactive",
#     "start_date_of_cycle": "2025-05-11",
#     "end_date_of_cycle": "2025-08-31",
#     "parameters": [
#         {
#             "name": "Overall Performance Rating",
#             "parameter_id": 296,
#             "helptext": "",
#             "employee": True,
#             "teamLead": True,
#             "fixed": True
#         }
#     ],
#     "stages": [
#         {
#             "name": "Setup",
#             "stage_id": 528,
#             "startDate": "2025-05-12",
#             "endDate": "2025-05-13"
#         },
#         {
#             "name": "Self Assessment",
#             "stage_id": 529,
#             "startDate": "2025-05-14",
#             "endDate": "2025-05-15"
#         },
#         {
#             "name": "Lead Assessment",
#             "stage_id": 530,
#             "startDate": "2025-05-16",
#             "endDate": "2025-05-17"
#         },
#         {
#             "name": "HR/VL Validation",
#             "stage_id": 531,
#             "startDate": "2025-05-18",
#             "endDate": "2025-05-19"
#         },
#         {
#             "name": "Closure",
#             "stage_id": 532,
#             "startDate": "2025-05-20",
#             "endDate": "2025-05-21"
#         }
#     ]
# }

#   response = client.put(f"/edit-appraisal-cycle/{cycle_id}", json=payload)
#   assert response.status_code == 200
#   assert response.json() == {"message": "Appraisal cycle updated successfully"}

# import pytest
# from unittest.mock import MagicMock, patch
# from fastapi import HTTPException
# from sqlalchemy.orm import Session

# # Import your actual modules (adjust these imports to match your project structure)
# from schema.edit_appraisal_cycle import CycleUpdate, Parameter, Stage
# from dao.edit_appraisal_cycle import edit_cycle
# from models import AppraisalCycle, Parameter as ParameterModel, Stage as StageModel
# from routes import edit_appraisal_cycle


# @pytest.fixture
# def mock_db():
#     """Create a mock database session for testing."""
#     db_mock = MagicMock(spec=Session)
    
#     # Setup query mocks
#     query_mock = MagicMock()
#     filter_mock = MagicMock()
#     first_mock = MagicMock()
    
#     # Setup the query chain
#     db_mock.query.return_value = query_mock
#     query_mock.filter.return_value = filter_mock
#     filter_mock.first.return_value = first_mock
    
#     return db_mock


# @pytest.fixture
# def sample_cycle_update():
#     """Create a sample CycleUpdate object for testing."""
#     parameters = [
#         Parameter(
#             name="Updated Parameter 1",
#             parameter_id=1,
#             helptext="Updated Help Text 1",
#             employee=True,
#             teamLead=True,
#             fixed=False
#         ),
#         Parameter(
#             name="New Parameter",
#             helptext="New Help Text",
#             employee=True,
#             teamLead=False,
#             fixed=True
#         )
#     ]
    
#     stages = [
#         Stage(
#             name="Updated Stage 1",
#             stage_id=1,
#             startDate="2025-02-01",
#             endDate="2025-05-31"
#         ),
#         Stage(
#             name="New Stage",
#             startDate="2025-06-01",
#             endDate="2025-11-30"
#         )
#     ]
    
#     return CycleUpdate(
#         cycle_name="Updated Cycle",
#         description="Updated Description",
#         status="Active",
#         start_date_of_cycle="2025-02-01",
#         end_date_of_cycle="2025-11-30",
#         parameters=parameters,
#         stages=stages
#     )


# def test_edit_cycle_success(mock_db, sample_cycle_update):
#     """Test successful editing of an appraisal cycle."""
#     # Setup
#     cycle_id = 1
#     existing_cycle = MagicMock(spec=AppraisalCycle)
#     existing_cycle.cycle_id = cycle_id
    
#     existing_param = MagicMock(spec=ParameterModel)
#     existing_param.parameter_id = 1
#     existing_param.cycle_id = cycle_id
    
#     existing_stage = MagicMock(spec=StageModel)
#     existing_stage.stage_id = 1
#     existing_stage.cycle_id = cycle_id
    
#     # Configure mock database to return our test objects
#     query_cycle = MagicMock()
#     query_cycle.filter.return_value.first.return_value = existing_cycle
    
#     query_param = MagicMock()
#     query_param.filter.return_value.first.return_value = existing_param
    
#     query_stage = MagicMock()
#     query_stage.filter.return_value.first.return_value = existing_stage
    
#     # Setup side effect for query method to return different mocks based on model class
#     def side_effect_query(model_class):
#         if model_class == AppraisalCycle:
#             return query_cycle
#         elif model_class == ParameterModel:
#             return query_param
#         elif model_class == StageModel:
#             return query_stage
#         return MagicMock()
    
#     mock_db.query.side_effect = side_effect_query
    
#     # Execute
#     result = edit_cycle(mock_db, cycle_id, sample_cycle_update)
    
#     # Assert
#     assert result["message"] == "Appraisal cycle updated successfully"
    
#     # Verify cycle updates
#     assert existing_cycle.cycle_name == sample_cycle_update.cycle_name
#     assert existing_cycle.description == sample_cycle_update.description
#     assert existing_cycle.status == sample_cycle_update.status
#     assert existing_cycle.start_date_of_cycle == sample_cycle_update.start_date_of_cycle
#     assert existing_cycle.end_date_of_cycle == sample_cycle_update.end_date_of_cycle
    
#     # Verify database operations
#     mock_db.commit.assert_called_once()
#     mock_db.refresh.assert_called_once_with(existing_cycle)
    
#     # Verify parameter updates
#     assert existing_param.parameter_title == sample_cycle_update.parameters[0].name
#     assert existing_param.helptext == sample_cycle_update.parameters[0].helptext
#     assert existing_param.applicable_to_employee == sample_cycle_update.parameters[0].employee
#     assert existing_param.applicable_to_lead == sample_cycle_update.parameters[0].teamLead
#     assert existing_param.is_fixed_parameter == sample_cycle_update.parameters[0].fixed
    
#     # Verify new parameter was added
#     mock_db.add.assert_called()  # At least one add call for the new parameter


# def test_edit_cycle_not_found(mock_db, sample_cycle_update):
#     """Test editing a non-existent appraisal cycle."""
#     # Setup
#     cycle_id = 999  # Non-existent ID
    
#     # Configure mock database to return None for the cycle
#     query_cycle = MagicMock()
#     query_cycle.filter.return_value.first.return_value = None
#     mock_db.query.return_value = query_cycle
    
#     # Execute and assert
#     with pytest.raises(HTTPException) as excinfo:
#         edit_cycle(mock_db, cycle_id, sample_cycle_update)
    
#     assert excinfo.value.status_code == 404
#     assert "not found" in excinfo.value.detail


# def test_edit_cycle_delete_parameters(mock_db, sample_cycle_update):
#     """Test deleting parameters during cycle update."""
#     # Setup
#     cycle_id = 1
#     existing_cycle = MagicMock(spec=AppraisalCycle)
#     existing_cycle.cycle_id = cycle_id
    
#     # Configure mock database
#     query_cycle = MagicMock()
#     query_cycle.filter.return_value.first.return_value = existing_cycle
    
#     query_param = MagicMock()
#     query_param_filter = MagicMock()
#     query_param_filter_notin = MagicMock()
#     query_param.filter.return_value = query_param_filter
#     query_param_filter.filter.return_value = query_param_filter_notin
    
#     def side_effect_query(model_class):
#         if model_class == AppraisalCycle:
#             return query_cycle
#         elif model_class == ParameterModel:
#             return query_param
#         return MagicMock()
    
#     mock_db.query.side_effect = side_effect_query
    
#     # Execute
#     result = edit_cycle(mock_db, cycle_id, sample_cycle_update)
    
#     # Assert
#     assert result["message"] == "Appraisal cycle updated successfully"
    
#     # Verify parameter deletion call
#     query_param_filter_notin.delete.assert_called_once_with(synchronize_session=False)


# def test_edit_cycle_update_existing_stage(mock_db, sample_cycle_update):
#     """Test updating an existing stage during cycle update."""
#     # Setup
#     cycle_id = 1
#     existing_cycle = MagicMock(spec=AppraisalCycle)
#     existing_cycle.cycle_id = cycle_id
    
#     existing_stage = MagicMock(spec=StageModel)
#     existing_stage.stage_id = 1
#     existing_stage.cycle_id = cycle_id
    
#     # Configure mock database
#     query_cycle = MagicMock()
#     query_cycle.filter.return_value.first.return_value = existing_cycle
    
#     query_stage = MagicMock()
#     query_stage.filter.return_value.first.return_value = existing_stage
    
#     def side_effect_query(model_class):
#         if model_class == AppraisalCycle:
#             return query_cycle
#         elif model_class == StageModel:
#             return query_stage
#         return MagicMock()
    
#     mock_db.query.side_effect = side_effect_query
    
#     # Execute
#     result = edit_cycle(mock_db, cycle_id, sample_cycle_update)
    
#     # Assert
#     assert result["message"] == "Appraisal cycle updated successfully"
    
#     # Verify stage updates
#     assert existing_stage.stage_name == sample_cycle_update.stages[0].name
#     assert existing_stage.start_date_of_stage == sample_cycle_update.stages[0].startDate
#     assert existing_stage.end_date_of_stage == sample_cycle_update.stages[0].endDate


# def test_edit_cycle_add_new_parameter(mock_db, sample_cycle_update):
#     """Test adding a new parameter during cycle update."""
#     # Setup
#     cycle_id = 1
#     existing_cycle = MagicMock(spec=AppraisalCycle)
#     existing_cycle.cycle_id = cycle_id
    
#     # Configure mock database - first parameter doesn't exist
#     query_cycle = MagicMock()
#     query_cycle.filter.return_value.first.return_value = existing_cycle
    
#     query_param = MagicMock()
#     query_param.filter.return_value.first.return_value = None  # No existing parameter
    
#     def side_effect_query(model_class):
#         if model_class == AppraisalCycle:
#             return query_cycle
#         elif model_class == ParameterModel:
#             return query_param
#         return MagicMock()
    
#     mock_db.query.side_effect = side_effect_query
    
#     # Execute
#     result = edit_cycle(mock_db, cycle_id, sample_cycle_update)
    
#     # Assert
#     assert result["message"] == "Appraisal cycle updated successfully"
    
#     # Verify new parameters were added
#     assert mock_db.add.call_count >= 2  # At least two parameters should be added


# @patch('app.dao.edit_cycle')
# def test_edit_appraisal_cycle_route_success(mock_edit_cycle, mock_db):
#     """Test the FastAPI route handler for successful cycle update."""
#     # Setup
#     cycle_id = 1
#     mock_cycle_data = MagicMock(spec=CycleUpdate)
#     mock_edit_cycle.return_value = {"message": "Appraisal cycle updated successfully"}
    
#     # Execute
#     result = edit_appraisal_cycle(cycle_id, mock_cycle_data, mock_db)
    
#     # Assert
#     assert result == {"message": {"message": "Appraisal cycle updated successfully"}}
#     mock_edit_cycle.assert_called_once_with(mock_db, cycle_id, mock_cycle_data)


# @patch('app.dao.edit_cycle')
# def test_edit_appraisal_cycle_route_exception(mock_edit_cycle, mock_db):
#     """Test the FastAPI route handler when an exception occurs."""
#     # Setup
#     cycle_id = 1
#     mock_cycle_data = MagicMock(spec=CycleUpdate)
#     mock_edit_cycle.side_effect = Exception("Test exception")
    
#     # Execute and assert
#     with pytest.raises(HTTPException) as excinfo:
#         edit_appraisal_cycle(cycle_id, mock_cycle_data, mock_db)
    
#     assert excinfo.value.status_code == 500
#     assert "Internal server error" in excinfo.value.detail

import pytest
from unittest.mock import MagicMock, patch
from fastapi import HTTPException
from sqlalchemy.orm import Session

# Import your actual modules (adjusted to match your project structure)
# Check these imports and modify them based on your actual structure
from schema.edit_appraisal_cycle import Parameter, Stage
from pydantic import BaseModel
from typing import List, Optional

# Create CycleUpdate class if it doesn't exist in your schema file
class CycleUpdate(BaseModel):
    cycle_name: str
    description: str
    status: str
    start_date_of_cycle: str
    end_date_of_cycle: str
    parameters: List[Parameter]
    stages: List[Stage]

# Import your actual models and functions (adjust paths as needed)
from dao.edit_appraisal_cycle import edit_cycle
from models.edit_appraisal_cycle import AppraisalCycle, Parameter as ParameterModel, Stage as StageModel
from routes.edit_appraisal_cycle import edit_appraisal_cycle


@pytest.fixture
def mock_db():
    """Create a mock database session for testing."""
    db_mock = MagicMock(spec=Session)
    
    # Setup query mocks
    query_mock = MagicMock()
    filter_mock = MagicMock()
    first_mock = MagicMock()
    
    # Setup the query chain
    db_mock.query.return_value = query_mock
    query_mock.filter.return_value = filter_mock
    filter_mock.first.return_value = first_mock
    
    return db_mock


@pytest.fixture
def sample_cycle_update():
    """Create a sample CycleUpdate object for testing."""
    parameters = [
        Parameter(
            name="Updated Parameter 1",
            parameter_id=1,
            helptext="Updated Help Text 1",
            employee=True,
            teamLead=True,
            fixed=False
        ),
        Parameter(
            name="New Parameter",
            helptext="New Help Text",
            employee=True,
            teamLead=False,
            fixed=True
        )
    ]
    
    stages = [
        Stage(
            name="Updated Stage 1",
            stage_id=1,
            startDate="2025-02-01",
            endDate="2025-05-31"
        ),
        Stage(
            name="New Stage",
            startDate="2025-06-01",
            endDate="2025-11-30"
        )
    ]
    
    return CycleUpdate(
        cycle_name="Updated Cycle",
        description="Updated Description",
        status="Active",
        start_date_of_cycle="2025-02-01",
        end_date_of_cycle="2025-11-30",
        parameters=parameters,
        stages=stages
    )


def test_edit_cycle_success(mock_db, sample_cycle_update):
    """Test successful editing of an appraisal cycle."""
    # Setup
    cycle_id = 1
    existing_cycle = MagicMock(spec=AppraisalCycle)
    existing_cycle.cycle_id = cycle_id
    
    existing_param = MagicMock(spec=ParameterModel)
    existing_param.parameter_id = 1
    existing_param.cycle_id = cycle_id
    
    existing_stage = MagicMock(spec=StageModel)
    existing_stage.stage_id = 1
    existing_stage.cycle_id = cycle_id
    
    # Configure mock database to return our test objects
    query_cycle = MagicMock()
    query_cycle.filter.return_value.first.return_value = existing_cycle
    
    query_param = MagicMock()
    query_param.filter.return_value.first.return_value = existing_param
    
    query_stage = MagicMock()
    query_stage.filter.return_value.first.return_value = existing_stage
    
    # Setup side effect for query method to return different mocks based on model class
    def side_effect_query(model_class):
        if model_class == AppraisalCycle:
            return query_cycle
        elif model_class == ParameterModel:
            return query_param
        elif model_class == StageModel:
            return query_stage
        return MagicMock()
    
    mock_db.query.side_effect = side_effect_query
    
    # Execute
    result = edit_cycle(mock_db, cycle_id, sample_cycle_update)
    
    # Assert
    assert result["message"] == "Appraisal cycle updated successfully"
    
    # Verify cycle updates
    assert existing_cycle.cycle_name == sample_cycle_update.cycle_name
    assert existing_cycle.description == sample_cycle_update.description
    assert existing_cycle.status == sample_cycle_update.status
    assert existing_cycle.start_date_of_cycle == sample_cycle_update.start_date_of_cycle
    assert existing_cycle.end_date_of_cycle == sample_cycle_update.end_date_of_cycle
    
    # Verify database operations
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(existing_cycle)
    
    # Verify parameter updates
    assert existing_param.parameter_title == sample_cycle_update.parameters[0].name
    assert existing_param.helptext == sample_cycle_update.parameters[0].helptext
    assert existing_param.applicable_to_employee == sample_cycle_update.parameters[0].employee
    assert existing_param.applicable_to_lead == sample_cycle_update.parameters[0].teamLead
    assert existing_param.is_fixed_parameter == sample_cycle_update.parameters[0].fixed
    
    # Verify new parameter was added
    mock_db.add.assert_called()  # At least one add call for the new parameter


def test_edit_cycle_not_found(mock_db, sample_cycle_update):
    """Test editing a non-existent appraisal cycle."""
    # Setup
    cycle_id = 999  # Non-existent ID
    
    # Configure mock database to return None for the cycle
    query_cycle = MagicMock()
    query_cycle.filter.return_value.first.return_value = None
    mock_db.query.return_value = query_cycle
    
    # Execute and assert
    with pytest.raises(HTTPException) as excinfo:
        edit_cycle(mock_db, cycle_id, sample_cycle_update)
    
    assert excinfo.value.status_code == 404
    assert "not found" in excinfo.value.detail


def test_edit_cycle_delete_parameters(mock_db, sample_cycle_update):
    """Test deleting parameters during cycle update."""
    # Setup
    cycle_id = 1
    existing_cycle = MagicMock(spec=AppraisalCycle)
    existing_cycle.cycle_id = cycle_id
    
    # Configure mock database
    query_cycle = MagicMock()
    query_cycle.filter.return_value.first.return_value = existing_cycle
    
    query_param = MagicMock()
    query_param_filter = MagicMock()
    query_param_filter_notin = MagicMock()
    query_param.filter.return_value = query_param_filter
    query_param_filter.filter.return_value = query_param_filter_notin
    
    def side_effect_query(model_class):
        if model_class == AppraisalCycle:
            return query_cycle
        elif model_class == ParameterModel:
            return query_param
        return MagicMock()
    
    mock_db.query.side_effect = side_effect_query
    
    # Execute
    result = edit_cycle(mock_db, cycle_id, sample_cycle_update)
    
    # Assert
    assert result["message"] == "Appraisal cycle updated successfully"
    
    # Verify parameter deletion call
    query_param_filter_notin.delete.assert_called_once_with(synchronize_session=False)


def test_edit_cycle_update_existing_stage(mock_db, sample_cycle_update):
    """Test updating an existing stage during cycle update."""
    # Setup
    cycle_id = 1
    existing_cycle = MagicMock(spec=AppraisalCycle)
    existing_cycle.cycle_id = cycle_id
    
    existing_stage = MagicMock(spec=StageModel)
    existing_stage.stage_id = 1
    existing_stage.cycle_id = cycle_id
    
    # Configure mock database
    query_cycle = MagicMock()
    query_cycle.filter.return_value.first.return_value = existing_cycle
    
    query_stage = MagicMock()
    query_stage.filter.return_value.first.return_value = existing_stage
    
    def side_effect_query(model_class):
        if model_class == AppraisalCycle:
            return query_cycle
        elif model_class == StageModel:
            return query_stage
        return MagicMock()
    
    mock_db.query.side_effect = side_effect_query
    
    # Execute
    result = edit_cycle(mock_db, cycle_id, sample_cycle_update)
    
    # Assert
    assert result["message"] == "Appraisal cycle updated successfully"
    
    # Verify stage updates
    assert existing_stage.stage_name == sample_cycle_update.stages[0].name
    assert existing_stage.start_date_of_stage == sample_cycle_update.stages[0].startDate
    assert existing_stage.end_date_of_stage == sample_cycle_update.stages[0].endDate


def test_edit_cycle_add_new_parameter(mock_db, sample_cycle_update):
    """Test adding a new parameter during cycle update."""
    # Setup
    cycle_id = 1
    existing_cycle = MagicMock(spec=AppraisalCycle)
    existing_cycle.cycle_id = cycle_id
    
    # Configure mock database - first parameter doesn't exist
    query_cycle = MagicMock()
    query_cycle.filter.return_value.first.return_value = existing_cycle
    
    query_param = MagicMock()
    query_param.filter.return_value.first.return_value = None  # No existing parameter
    
    def side_effect_query(model_class):
        if model_class == AppraisalCycle:
            return query_cycle
        elif model_class == ParameterModel:
            return query_param
        return MagicMock()
    
    mock_db.query.side_effect = side_effect_query
    
    # Execute
    result = edit_cycle(mock_db, cycle_id, sample_cycle_update)
    
    # Assert
    assert result["message"] == "Appraisal cycle updated successfully"
    
    # Verify new parameters were added
    assert mock_db.add.call_count >= 2  # At least two parameters should be added


@patch('dao.appraisal_dao.edit_cycle')  # Adjust this path to match your actual import path
def test_edit_appraisal_cycle_route_success(mock_edit_cycle, mock_db):
    """Test the FastAPI route handler for successful cycle update."""
    # Setup
    cycle_id = 1
    mock_cycle_data = MagicMock(spec=CycleUpdate)
    mock_edit_cycle.return_value = {"message": "Appraisal cycle updated successfully"}
    
    # Execute
    result = edit_appraisal_cycle(cycle_id, mock_cycle_data, mock_db)
    
    # Assert
    assert result == {"message": {"message": "Appraisal cycle updated successfully"}}
    mock_edit_cycle.assert_called_once_with(mock_db, cycle_id, mock_cycle_data)


@patch('dao.appraisal_dao.edit_cycle')  # Adjust this path to match your actual import path
def test_edit_appraisal_cycle_route_exception(mock_edit_cycle, mock_db):
    """Test the FastAPI route handler when an exception occurs."""
    # Setup
    cycle_id = 1
    mock_cycle_data = MagicMock(spec=CycleUpdate)
    mock_edit_cycle.side_effect = Exception("Test exception")
    
    # Execute and assert
    with pytest.raises(HTTPException) as excinfo:
        edit_appraisal_cycle(cycle_id, mock_cycle_data, mock_db)
    
    assert excinfo.value.status_code == 500
    assert "Internal server error" in excinfo.value.detail