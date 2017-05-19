from models import Category
from models import Measurement
from datetime import datetime


class Tracker(object):
    """The tracker"""

    def __init__(self, session):
        """Initialize a new tracker from the database session."""
        self._session = session

    def has_category(self, name):
        """Check that the category exists."""
        category = self._session.query(Category).filter_by(name=name).first()
        if category:
            return True
        else:
            return False

    def create_category(self, name, is_integer=False):
        """Create a new category."""
        if not self.has_category(name):
            category = Category(name=name, is_integer=is_integer)
            self._session.add(category)
            self._session.commit()
        else:
            raise ValueError("The '{}' category has already exists!".format(name))

    def is_integer_category(self, name):
        """Check that the category is integer."""
        if self.has_category(name):
            category = self._session.query(Category).filter_by(name=name).first()
            return category.is_integer
        else:
            raise ValueError("The '{}' category is missing!".format(name))

    def list_categories(self):
        """List the names of the categories."""
        categories = self._session.query(Category).all()
        return [category.name for category in categories]

    def rename_category(self, old_name, new_name):
        """Rename the category."""
        if not self.has_category(old_name):
            raise ValueError("Unable to rename, because '{}' does not exist!".format(old_name))
        if self.has_category(new_name):
            raise ValueError("Unable to rename, because '{}' already exist!".format(new_name))
        category = self._session.query(Category).filter_by(name=old_name).first()
        category.name = new_name
        self._session.add(category)
        self._session.commit()

    def correct_value_type(self, name, is_integer):
        """Correct the type of the measure types of the category."""
        if not self.has_category(name):
            raise ValueError("Unable to correct value type because '{}' does not exist!".format(name))
        category = self._session.query(Category).filter_by(name=name).first()
        category.is_integer = is_integer
        self._session.add(category)
        self._session.commit()

    def remove_category(self, name):
        """Remove the category."""
        if not self.has_category(name):
            raise ValueError("Unable to remove '{}' because it does not exist!")
        category = self._session.query(Category).filter_by(name=name).first()
        self._session.delete(category)
        self._session.commit()

    def save_measurement(self, name, value):
        """Save the given measure."""
        if not self.has_category(name):
            raise ValueError("Unable to save because the category '{}' does not exist!".format(name))
        category = self._session.query(Category).filter_by(name=name).first()
        measurement = Measurement(value=value, category=category, timestamp=datetime.now())
        self._session.add(measurement)
        self._session.commit()

    def list_measurements(self, name):
        """Get all measurements of the category."""
        if not self.has_category(name):
            raise ValueError("The category '{}' does not exist!".format(name))
        category = self._session.query(Category).filter_by(name=name).first()
        return [measurement for measurement in category.measurements]

    def correct_measurement(self, measurement_id, value):
        """Update the value of the measurement."""
        measurement = self._session.query(Measurement).filter_by(id=measurement_id).first()
        if measurement:
            measurement.value = value
            self._session.add(measurement)
            self._session.commit()
        else:
            raise ValueError("The {} is an invalid measure identifier!".format(measurement_id))

    def remove_measurement(self, measurement_id):
        """Remove the measurement."""
        measurement = self._session.query(Measurement).filter_by(id=measurement_id).first()
        if measurement:
            self._session.delete(measurement)
            self._session.commit()
        else:
            raise ValueError("The {} is an invalid measure identifier!".format(measurement_id))
