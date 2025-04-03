
from sqlalchemy.orm import Session
from models.parameters import Parameter

def get_all_parameters(db: Session):
    """ Fetch all parameters from the database. """
    return db.query(Parameter).all()

def get_parameter_by_id(db: Session, parameter_id: int):
    """ Fetch a single parameter by ID. """
    return db.query(Parameter).filter(Parameter.parameter_id == parameter_id).first()

def add_parameter(db: Session, parameter_data):
    """ Add a new parameter to the database. """
    new_parameter = Parameter(**parameter_data)
    db.add(new_parameter)
    db.commit()
    db.refresh(new_parameter)
    return new_parameter

def get_parameters_for_cycle(db: Session, cycle_id: int, is_lead: bool):
    """Fetch parameters for a given cycle based on employee role"""
    return db.query(Parameter).filter(
        Parameter.cycle_id == cycle_id,
        (Parameter.applicable_to_lead if is_lead else Parameter.applicable_to_employee) == True
    ).all()
