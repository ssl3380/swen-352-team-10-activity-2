import json
import os
import unittest
from unittest.mock import Mock

from tests_data import get_test_data
from library.ext_api_interface import *

ext_api_interface_tests_data = get_test_data.get_test_data_path()


class TestBooksAPI(unittest.TestCase):
    def setUp(self):
        self.api = Books_API()
        self.book = "concurrency in go"
        self.e_book = "software architecture in practice"
        self.book_dne = "mig in the dark"
        self.author = "Katherine Cox-Buday"
        with open(os.path.join(ext_api_interface_tests_data, 'ebooks.txt'), 'r') as f:
            self.e_books_data = json.loads(f.read())
        with open(os.path.join(ext_api_interface_tests_data, 'book_found_ebook.txt'), 'r') as f:
            self.e_book_payload_data = json.loads(f.read())
        with open(os.path.join(ext_api_interface_tests_data, 'books.txt'), 'r') as f:
            self.books_data = json.loads(f.read())
        with open(os.path.join(ext_api_interface_tests_data, 'book_found_data.txt'), 'r') as f:
            self.book_found_json_data = json.loads(f.read())
        with open(os.path.join(ext_api_interface_tests_data, 'books_by_author.txt'), 'r') as f:
            self.books_by_author = json.loads(f.read())
        with open(os.path.join(ext_api_interface_tests_data, 'books_by_author_response.txt'), 'r') as f:
            self.books_by_author_response = json.loads(f.read())

    def test_make_request(self):
        attr = {'json.return_value': dict()}
        requests.get = Mock(return_value=Mock(status_code=200, **attr))
        self.assertEqual(self.api.make_request(""), dict())

        requests.get = Mock(return_value=Mock(status_code=202, **attr))
        self.assertEqual(self.api.make_request(""), None)

        requests.get = Mock(side_effect=requests.ConnectionError("Mocked ConnectionError"))
        self.assertEqual(self.api.make_request(""), None)

    def test_is_book_available(self):
        json_data_book_not_found = {"numFound": 0, "start": 0, "numFoundExact": True,
                                    "docs": [], "num_found": 0, "q": self.book_dne,
                                    "offset": None}
        self.api.make_request = Mock(return_value=json_data_book_not_found)
        self.assertEqual(self.api.is_book_available(self.book_dne), False)

        self.api.make_request = Mock(return_value=self.book_found_json_data)
        self.assertEqual(self.api.is_book_available(self.book), True)

    def test_books_by_author(self):
        json_data_book_not_found = None
        self.api.make_request = Mock(return_value=json_data_book_not_found)
        self.assertEqual(self.api.books_by_author(self.book_dne), [])

        self.api.make_request = Mock(return_value=self.books_by_author_response)
        self.assertEqual(self.api.books_by_author(self.author), self.books_by_author)

    def test_get_book_info(self):
        json_data_book_not_found = None
        self.api.make_request = Mock(return_value=json_data_book_not_found)
        self.assertEqual(self.api.get_book_info(self.book_dne), [])

        self.api.make_request = Mock(return_value=self.book_found_json_data)
        self.assertEqual(self.api.get_book_info(self.book), self.books_data)

    def test_get_ebooks(self):
        json_data_book_not_found = None
        self.api.make_request = Mock(return_value=json_data_book_not_found)
        self.assertEqual(self.api.get_ebooks(self.book_dne), [])

        self.api.make_request = Mock(return_value=self.e_book_payload_data)
        self.assertEqual(self.api.get_ebooks(self.e_book), self.e_books_data)


if __name__ == "__main__":
    unittest.main()
