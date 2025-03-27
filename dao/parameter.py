
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

