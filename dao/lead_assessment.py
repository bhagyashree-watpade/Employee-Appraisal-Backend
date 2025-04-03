
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
            raise ValueError("Employee is not allocated to this cycle.")

        changes_made = False  # Flag to track if any updates were made

        # Iterate over provided ratings and save or update them
        for rating in ratings:
            param_id = rating["parameter_id"]
            param_rating = rating["parameter_rating"]
            specific_input = rating.get("specific_input", "")

            # Validate if the parameter exists
            parameter = db.query(Parameter).filter(Parameter.parameter_id == param_id).first()
            if not parameter:
                raise ValueError(f"Invalid parameter ID: {param_id}")

            # Validate rating range
            if param_rating < 1 or param_rating > 4:
                raise ValueError(f"Invalid rating for parameter {param_id}. Must be between 1 and 4.")

            # Check if a record already exists for this parameter
            existing_rating = db.query(LeadAssessmentRating).filter(
                LeadAssessmentRating.allocation_id == allocation.allocation_id,
                LeadAssessmentRating.cycle_id == cycle_id,
                LeadAssessmentRating.employee_id == employee_id,
                LeadAssessmentRating.parameter_id == param_id
            ).first()

            if existing_rating:
                # Check if anything has changed
                if (existing_rating.parameter_rating != param_rating or 
                    existing_rating.specific_input != specific_input or
                    existing_rating.discussion_date != discussion_date):

                    # Update existing record
                    existing_rating.parameter_rating = param_rating
                    existing_rating.specific_input = specific_input
                    existing_rating.discussion_date = discussion_date
                    changes_made = True  # Mark that an update was done
            else:
                # Insert a new record if it doesn't exist
                new_rating = LeadAssessmentRating(
                    allocation_id=allocation.allocation_id,
                    cycle_id=cycle_id,
                    employee_id=employee_id,
                    parameter_id=param_id,
                    parameter_rating=param_rating,
                    specific_input=specific_input,
                    discussion_date=discussion_date
                )
                db.add(new_rating)
                changes_made = True  # Mark that an insert was done

        if changes_made:
            db.commit()
            return {"message": "Lead assessment rating saved successfully."}
        else:
            return {"message": "No changes detected."}

    except ValueError as ve:
        db.rollback()
        raise ve

    except SQLAlchemyError:
        db.rollback()
        raise Exception("Database error occurred while saving ratings.")
