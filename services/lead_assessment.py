
from sqlalchemy.orm import Session
from models.lead_assessment import LeadAssessmentRating
from models.employee_allocation import EmployeeAllocation
from models.appraisal_cycle import AppraisalCycle
from models.parameters import Parameter
from sqlalchemy.exc import SQLAlchemyError

def save_lead_assessment_rating(db: Session, cycle_id: int, employee_id: int, ratings: list, discussion_date):
    try:
        # Validate if the appraisal cycle is active
        active_cycle = db.query(AppraisalCycle).filter(
            AppraisalCycle.cycle_id == cycle_id,
            AppraisalCycle.status == "active"
        ).first()

        if not active_cycle:
            raise ValueError("The selected appraisal cycle is not active.")

        # Check if the employee is allocated to the cycle
        allocation = db.query(EmployeeAllocation).filter(
            EmployeeAllocation.cycle_id == cycle_id,
            EmployeeAllocation.employee_id == employee_id
        ).first()

        if not allocation:
            raise ValueError("No allocation found")  # ✅ Specific error message for 404

        # Iterate over provided ratings and save them
        for rating in ratings:
            # Validate if the parameter exists
            parameter = db.query(Parameter).filter(Parameter.parameter_id == rating["parameter_id"]).first()
            if not parameter:
                raise ValueError(f"Invalid parameter ID: {rating['parameter_id']}")

            # Validate rating range
            if rating["parameter_rating"] < 1 or rating["parameter_rating"] > 4:
                raise ValueError(f"Invalid rating for parameter {rating['parameter_id']}. Must be between 1 and 4.")

            # Create and save the rating
            lead_rating = LeadAssessmentRating(
                allocation_id=allocation.allocation_id,
                cycle_id=cycle_id,
                employee_id=employee_id,
                parameter_id=rating["parameter_id"],
                parameter_rating=rating["parameter_rating"],
                specific_input=rating.get("specific_input", ""),
                discussion_date=discussion_date
            )
            db.add(lead_rating)

        db.commit()
        return {"message": "Lead assessment rating saved successfully."}

    except ValueError as ve:
        db.rollback()
        raise ve  # ✅ Ensures the router can catch the "No allocation found" error.

    except SQLAlchemyError as e:
        db.rollback()
        raise Exception("Database error occurred while saving ratings.")
