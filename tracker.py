from models import session
from models import Category
from models import Measurement
from datetime import datetime


def has_category(name):
    """Check that the category exists."""
    category = session.query(Category).filter_by(name=name).first()
    if category:
        return True
    else:
        return False


def create_category(name, is_integer=False):
    """Create a new category."""
    if not has_category(name):
        category = Category(name=name, is_integer=is_integer)
        session.add(category)
        session.commit()
    else:
        raise ValueError("The '{}' category has already exists!".format(name))


def list_categories():
    """List the names of the categories."""
    categories = session.query(Category).all()
    return [category.name for category in categories]


def rename_category(old_name, new_name):
    """Rename the category."""
    if not has_category(old_name):
        raise ValueError("Unable to rename, because '{}' does not exist!".format(old_name))
    if has_category(new_name):
        raise ValueError("Unable to rename, because '{}' already exist!".format(new_name))
    category = session.query(Category).filter_by(name=old_name).first()
    category.name = new_name
    session.add(category)
    session.commit()


def correct_value_type(name, is_integer):
    """Correct the type of the measure types of the category."""
    if not has_category(name):
        raise ValueError("Unable to correct value type because '{}' does not exist!".format(name))
    category = session.query(Category).filter_by(name=name).first()
    category.is_integer = is_integer
    session.add(category)
    session.commit()


def remove_category(name):
    """Remove the category."""
    if not has_category(name):
        raise ValueError("Unable to remove '{}' because it does not exist!")
    category = session.query(Category).filter_by(name=name).first()
    session.delete(category)
    session.commit()


def save_measurement(name, value):
    """Save the given measure."""
    if not has_category(name):
        raise ValueError("Unable to save because the category '{}' does not exist!".format(name))
    category = session.query(Category).filter_by(name=name).first()
    measurement = Measurement(value=value, category=category, timestamp=datetime.now())
    session.add(measurement)
    session.commit()


def list_measurements(name):
    """Get all measurements of the category."""
    if not has_category(name):
        raise ValueError("The category '{}' does not exist!".format(name))
    category = session.query(Category).filter_by(name=name).first()
    return [measurement for measurement in category.measurements]


def correct_measurement(measurement_id, value):
    """Update the value of the measurement."""
    measurement = session.query(Measurement).filter_by(id=measurement_id).first()
    if measurement:
        measurement.value = value
        session.add(measurement)
        session.commit()
    else:
        raise ValueError("The {} is an invalid measure identifier!".format(measurement_id))


def remove_measurement(measurement_id):
    """Remove the measurement."""
    measurement = session.query(Measurement).filter_by(id=measurement_id).first()
    if measurement:
        session.delete(measurement)
        session.commit()
    else:
        raise ValueError("The {} is an invalid measure identifier!".format(measurement_id))
