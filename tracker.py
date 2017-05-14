from models import session
from models import Category


class Tracker(object):
    """Represents the tracker"""

    def __init__(self):
        category = Category(name='Trials', is_integer=True)
        session.add(category)
        session.commit()
