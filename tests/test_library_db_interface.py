import unittest
from unittest.mock import Mock
from library import library_db_interface
from library.library_db_interface import *

class TestLibraryDBInterface(unittest.TestCase):

    def setUp(self):
        library_db_interface.TinyDB = Mock()
        library_db_interface.Patron = Mock()
        library_db_interface.Query = Mock()
        self.interface = Library_DB()

    def test_constructor(self):
        self.assertIsNotNone(self.interface.DATABASE_FILE, 'db file pointing to None')
        self.assertEqual('db.json', self.interface.DATABASE_FILE, 'pulling incorrect db file')

    def test_close_db(self):
        self.interface.db.close = Mock()
        self.interface.close_db()
        self.interface.db.close.assert_called_once()

    def test_get_all_patrons(self):
        self.interface.db.all = Mock(return_value=['test1', 'test2'])
        result = self.interface.get_all_patrons()
        self.assertEqual(['test1', 'test2'], result, 'failed to get all patrons')

    def test_patron_count(self):
        self.interface.db.all = Mock(return_value=['test1', 'test2'])
        result = self.interface.get_patron_count()
        self.assertEqual(2, result, 'failed to get correct patron count')

    def test_insert_patron_good(self):
        patron = Mock()
        self.interface.retrieve_patron = Mock(return_value=None)
        patron.get_memberID = Mock(return_value='abc123')
        self.interface.convert_patron_to_db_format = Mock(return_value={'test': 'test'})
        self.interface.db.insert = Mock(return_value=123)
        result = self.interface.insert_patron(patron)

        patron.get_memberID.assert_called_once()
        self.interface.retrieve_patron.assert_called_once_with('abc123')
        self.interface.convert_patron_to_db_format.assert_called_once_with(patron)
        self.interface.db.insert.assert_called_once_with({'test': 'test'})
        self.assertEqual(123, result, 'failed to input patron correctly')

    def test_insert_patron_bad(self):
        self.interface.convert_patron_to_db_format = Mock();

        # patron is None
        patron = None
        result = self.interface.insert_patron(patron)
        self.assertEqual(None, result, 'failed to return None on patron being None')
        self.interface.convert_patron_to_db_format.assert_not_called()

        # patron exists
        patron = Mock()
        self.interface.retrieve_patron = Mock(return_value=patron)
        patron.get_memberID = Mock(return_value='abc123')
        result = self.interface.insert_patron(patron)
        self.assertEqual(None, result, 'failed to return None on patron already existing')
        self.interface.convert_patron_to_db_format.assert_not_called()

    def test_update_patron(self):

        # patron is None
        patron = None
        self.interface.convert_patron_to_db_format = Mock()
        result = self.interface.update_patron(patron)

        self.assertEqual(None, result, 'failed to return None on patron being None')
        self.interface.convert_patron_to_db_format.assert_not_called()

        # good path
        patron = Mock()
        self.interface.convert_patron_to_db_format = Mock(return_value={'test': 'test'})
        patron.get_memberID = Mock(return_value='abc123')
        self.interface.db.update = Mock()
        result = self.interface.update_patron(patron)

        self.interface.convert_patron_to_db_format.assert_called_once_with(patron)
        self.interface.db.update.assert_called_once_with({'test': 'test'}, False)

    def test_retrieve_patron(self):
        self.interface.db.search = Mock(return_value=[{'fname': 'test', 'lname': 'test', 'age': 22, 'memberID': 'abc123'}])
        result = self.interface.retrieve_patron('')
        self.interface.db.search.assert_called_once_with(False)
        self.assertIsNotNone(result, 'failed to retrieve patron correctly')

        self.interface.db.search = Mock(return_value=None)
        result = self.interface.retrieve_patron('')
        self.interface.db.search.assert_called_once_with(False)
        self.assertEqual(None, result, 'found no patron but failed to return None')

    def test_convert_patron_to_db_format(self):
        patron = Mock()
        patron.get_fname = Mock(return_value='testf')
        patron.get_lname = Mock(return_value='testl')
        patron.get_age = Mock(return_value=22)
        patron.get_memberID = Mock(return_value='abc123')
        patron.get_borrowed_books = Mock(return_value=['testbook'])

        result = self.interface.convert_patron_to_db_format(patron)
        mock_patron_dict = {'fname': 'testf', 'lname': 'testl', 'age': 22, 'memberID': 'abc123', 'borrowed_books': ['testbook']}
        self.assertEqual(mock_patron_dict, result)

