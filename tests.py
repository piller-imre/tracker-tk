import unittest

from models import create_database_session
from tracker import Tracker


class TrackerTest(unittest.TestCase):
    """Unit test for the tracker"""

    def setUp(self):
        """Set up a new database session."""
        session = create_database_session('sqlite:///:memory:')
        self._tracker = Tracker(session)

    def test_empty_categories(self):
        has_category = self._tracker.has_category("anything")
        self.assertFalse(has_category)


if __name__ == '__main__':
    unittest.main()
