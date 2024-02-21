import unittest
from unittest.mock import Mock
from library import library
import json

class TestLibrary(unittest.TestCase):

    def setUp(self):
        library.Library_DB = Mock()
        library.Books_API  = Mock()
        library.patron = Mock()
        self.lib = library.Library()
        with open('tests_data/ebooks.txt', 'r') as f:
            self.books_data = json.loads(f.read())
        with open('tests_data/book_titles.txt', 'r') as f:
            self.book_titles = json.loads(f.read())



    def test_is_ebook_true(self):
        self.lib.api.get_ebooks = Mock(return_value=self.books_data)
        self.assertTrue(self.lib.is_ebook('learning python'))

    def test_get_ebooks_count(self):
        self.lib.api.get_ebooks = Mock(return_value=self.books_data)
        self.assertEqual(self.lib.get_ebooks_count("learning python"), 8)

    def test_is_book_by_author(self):
        self.lib.api.books_by_author = Mock(return_value=self.book_titles)
        self.assertTrue(self.lib.is_book_by_author("Mark Lutz", "learning python"))

    def test_is_not_book_by_author(self):
        self.lib.api.books_by_author = Mock(return_value=self.book_titles)
        self.assertFalse(self.lib.is_book_by_author("Mark Lutz", "enabling python"))

    def test_get_languages_for_book(self):
        self.lib.api.get_book_info = Mock(return_value=self.books_data)
        self.assertEqual(self.lib.get_languages_for_book('learning python'), set(["eng"]))

    def test_register_patron(self):
        self.lib.db.insert_patron = Mock(return_value=2)
        self.assertEqual(self.lib.register_patron('John', 'Smith', '24', '2'), 2)

    def test_is_patron_registered(self):
        self.lib.db.retrieve_patron = Mock(return_value=library.patron)
        self.assertTrue(self.lib.is_patron_registered(library.patron))

    def test_borrow_book(self):
        self.lib.borrow_book('learning python', library.patron)
        library.patron.add_borrowed_book.assert_called()

    def test_return_borrowed_book(self):
        self.lib.return_borrowed_book('learning python', library.patron)
        library.patron.return_borrowed_book.assert_called()

    def test_is_book_borrowed(self):
        library.patron.get_borrowed_books = Mock(return_value=self.book_titles)
        self.assertTrue(self.lib.is_book_borrowed('learning python', library.patron))