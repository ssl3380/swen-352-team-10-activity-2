import unittest
from library.patron import *

class TestPatron(unittest.TestCase):

    def setUp(self):
        self.patron = Patron('safe_first', 'safe_last', 22, 'abc123')

    def test_good_constructor(self):
        self.assertEqual('safe_first', self.patron.fname, 'fname not constructed correctly')
        self.assertEqual('safe_last', self.patron.lname, 'lname not constructed correctly')
        self.assertEqual(22, self.patron.age, 'age not constructed correctly')
        self.assertEqual('abc123', self.patron.memberID, 'memberID not constructed correctly')

    def test_bad_constructor(self):
        self.assertRaises(InvalidNameException, Patron, "bad_first1", 'safe_last', 22, 'abc123')
        self.assertRaises(InvalidNameException, Patron, "safe_firsts", 'bad_last1', 22, 'abc123')

    def test_add_borrowed_book(self):
        self.patron.add_borrowed_book('test book')
        self.assertTrue('test book' in self.patron.borrowed_books, 'failed to add book')

        self.patron.add_borrowed_book('test book')
        self.assertEqual(1, self.patron.borrowed_books.count('test book'), 'added duplicate book')

        self.patron.add_borrowed_book('TEST BOOK')
        self.assertEqual(1, self.patron.borrowed_books.count('test book'), 'failed to ignore casing')

    def test_get_borrowed_books(self):
        self.patron.add_borrowed_book('test book')
        self.assertEqual(['test book'], self.patron.get_borrowed_books(), 'failed to return correct borrowed books')

    def test_return_borrowed_book(self):
        self.patron.add_borrowed_book('test book')
        self.patron.return_borrowed_book('test book')
        self.assertEqual([], self.patron.borrowed_books, 'failed to return book')

        self.patron.add_borrowed_book('test book')
        self.patron.return_borrowed_book('TEST BOOK')
        self.assertEqual([], self.patron.borrowed_books, 'failed to ignore casing')

        self.patron.add_borrowed_book('test book')
        self.patron.return_borrowed_book('test book 2: revenge')
        self.assertEqual(['test book'], self.patron.borrowed_books, 'incorrectly returned a book not intended to return')

    def test_equality(self):
        self.copy_cat = Patron('safe_first', 'safe_last', 22, 'abc123')
        self.imposter = Patron('freaky', 'bob', 59, '123abc')
        self.assertTrue(self.copy_cat == self.patron, 'failed to match equivalent patrons')
        self.assertFalse(self.imposter == self.patron, 'incorrectly matched not-equivalent patrons')
        self.assertTrue(self.imposter != self.patron, 'incorrectly matched not-equivalent patrons')

    def test_getters(self):
        self.assertEqual('safe_first', self.patron.get_fname(), 'failed to get fname correctly')
        self.assertEqual('safe_last', self.patron.get_lname(), 'failed to get lname correctly')
        self.assertEqual(22, self.patron.get_age(), 'failed to get age correctly')
        self.assertEqual('abc123', self.patron.get_memberID(), 'failed to get memberID correctly')