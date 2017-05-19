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

    def test_one_category(self):
        self._tracker.create_category('one')
        self.assertTrue(self._tracker.has_category("one"))
        self.assertFalse(self._tracker.has_category("two"))

    def test_two_categories(self):
        self._tracker.create_category('one')
        self._tracker.create_category('two')
        self.assertTrue(self._tracker.has_category("one"))
        self.assertTrue(self._tracker.has_category("two"))

    def test_duplicated_category_creation(self):
        self._tracker.create_category('one')
        with self.assertRaises(ValueError):
            self._tracker.create_category('one')

    def test_default_category_type(self):
        self._tracker.create_category('one')
        self.assertFalse(self._tracker.is_integer_category('one'))

    def test_non_integer_category(self):
        self._tracker.create_category('one', is_integer=False)
        self.assertFalse(self._tracker.is_integer_category('one'))

    def test_empty_categories_listing(self):
        self.assertEqual(self._tracker.list_categories(), [])

    def test_multiple_categories_listing(self):
        self._tracker.create_category('one')
        self._tracker.create_category('two')
        self.assertEqual(self._tracker.list_categories(), ['one', 'two'])

    def test_category_renaming(self):
        self._tracker.create_category('one')
        self._tracker.create_category('two')
        self._tracker.rename_category('two', 'three')
        self.assertEqual(self._tracker.list_categories(), ['one', 'three'])

    def test_missing_category_renaming(self):
        self._tracker.create_category('one')
        with self.assertRaises(ValueError):
            self._tracker.rename_category('two', 'three')

    def test_invalid_category_renaming(self):
        self._tracker.create_category('one')
        self._tracker.create_category('two')
        with self.assertRaises(ValueError):
            self._tracker.rename_category('two', 'one')

    def test_value_type_correction(self):
        self._tracker.create_category('one')
        self._tracker.correct_value_type('one', is_integer=True)
        self.assertTrue(self._tracker.is_integer_category('one'))

    def test_value_correction_to_integer(self):
        self._tracker.create_category('one', is_integer=True)
        self._tracker.correct_value_type('one', is_integer=False)
        self.assertFalse(self._tracker.is_integer_category('one'))

    def test_remove_category(self):
        self._tracker.create_category('one')
        self._tracker.create_category('two')
        self._tracker.remove_category('one')
        self.assertEqual(self._tracker.list_categories(), ['two'])

    def test_remove_invalid_category(self):
        self._tracker.create_category('one')
        self._tracker.create_category('two')
        with self.assertRaises(ValueError):
            self._tracker.remove_category('three')

    def test_save_measurement(self):
        self._tracker.create_category('scores')
        self._tracker.save_measurement('scores', 5)

    def test_missing_category_for_measurement(self):
        with self.assertRaises(ValueError):
            self._tracker.save_measurement('missing', 1)

    def test_empty_category_listing(self):
        self._tracker.create_category('scores')
        self.assertEqual(self._tracker.list_measurements('scores'), [])

    def test_measurement_listing(self):
        self._tracker.create_category('scores')
        self._tracker.save_measurement('scores', 5)
        self._tracker.save_measurement('scores', 6)
        self._tracker.save_measurement('scores', 7)
        measurements = self._tracker.list_measurements('scores')
        self.assertEqual(measurements[0].id, 1)
        self.assertEqual(measurements[1].id, 2)
        self.assertEqual(measurements[2].id, 3)
        self.assertEqual(measurements[0].value, 5)
        self.assertEqual(measurements[1].value, 6)
        self.assertEqual(measurements[2].value, 7)

    def test_missing_category_measurement_listing(self):
        with self.assertRaises(ValueError):
            _ = self._tracker.list_measurements('missing')

    def test_measurement_correction(self):
        self._tracker.create_category('scores')
        self._tracker.save_measurement('scores', 5)
        self._tracker.save_measurement('scores', 6)
        self._tracker.save_measurement('scores', 7)
        self._tracker.correct_measurement(1, 1)
        self._tracker.correct_measurement(2, 2)
        self._tracker.correct_measurement(3, 3)
        measurements = self._tracker.list_measurements('scores')
        self.assertEqual(measurements[0].id, 1)
        self.assertEqual(measurements[1].id, 2)
        self.assertEqual(measurements[2].id, 3)
        self.assertEqual(measurements[0].value, 1)
        self.assertEqual(measurements[1].value, 2)
        self.assertEqual(measurements[2].value, 3)

    def test_remove_measurement(self):
        self._tracker.create_category('scores')
        self._tracker.save_measurement('scores', 5)
        self._tracker.save_measurement('scores', 6)
        self._tracker.save_measurement('scores', 7)
        self._tracker.remove_measurement(2)
        measurements = self._tracker.list_measurements('scores')
        self.assertEqual(measurements[0].id, 1)
        self.assertEqual(measurements[1].id, 3)
        self.assertEqual(measurements[0].value, 5)
        self.assertEqual(measurements[1].value, 7)

    def test_remove_missing_measurement(self):
        self._tracker.create_category('scores')
        with self.assertRaises(ValueError):
            self._tracker.remove_measurement(1)


if __name__ == '__main__':
    unittest.main()
