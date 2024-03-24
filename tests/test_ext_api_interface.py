import json
import os
import unittest
from unittest.mock import Mock

from tests_data import get_test_data
from library.ext_api_interface import *

ext_api_interface_tests_data = get_test_data.get_test_data_path()


class TestBooksAPI(unittest.TestCase):
    API_URL = "http://openlibrary.org/search.json"

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
        self.assertIsNotNone(self.api.API_URL)
        self.assertEqual(self.API_URL, self.api.API_URL)
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

        request_url = "%s?q=%s" % (self.API_URL, self.book)
        self.api.make_request = Mock(return_value=self.book_found_json_data)
        self.assertEqual(self.api.is_book_available(self.book), True)
        self.api.make_request.assert_called_with(request_url)

        json_data_book_found_edge_case = {"numFound": 5, "start": 0, "numFoundExact": True, "docs": [
            {"key": "/works/OL28380841W", "type": "work",
             "seed": ["/books/OL49530107M", "/books/OL38858312M", "/works/OL28380841W",
                      "/subjects/go_(computer_program_language)",
                      "/subjects/concurrent_aggregates_(computer_program_language)", "/authors/OL7497128A"],
             "title": "Masteringconcurrencyingo", "title_sort": "Masteringconcurrencyingo",
             "title_suggest": "Masteringconcurrencyingo", "edition_count": 2,
             "edition_key": ["OL49530107M", "OL38858312M"], "publish_date": ["2014"], "publish_year": [2014],
             "first_publish_year": 2014, "oclc": ["887752715"], "lcc": ["QA-0076.73000000.G63.K699 20"],
             "isbn": ["9781783983490", "1783983493", "9781783983483", "1783983485"], "last_modified_i": 1694952915,
             "ebook_count_i": 0, "ebook_access": "no_ebook", "has_fulltext": False, "public_scan_b": False,
             "readinglog_count": 0, "want_to_read_count": 0, "currently_reading_count": 0, "already_read_count": 0,
             "publisher": ["Packt Publishing, Limited"], "language": ["eng"], "author_key": ["OL7497128A"],
             "author_name": ["Nathan Kozyra"],
             "subject": ["Go (Computer program language)", "Concurrent Aggregates (Computer program language)"],
             "publisher_facet": ["Packt Publishing, Limited"],
             "subject_facet": ["Concurrent Aggregates (Computer program language)", "Go (Computer program language)"],
             "_version_": 1777286953638559745, "lcc_sort": "QA-0076.73000000.G63.K699 20",
             "author_facet": ["OL7497128A Nathan Kozyra"],
             "subject_key": ["concurrent_aggregates_(computer_program_language)", "go_(computer_program_language)"]}],
                                          "num_found": 0, "q": self.book_dne,
                                          "offset": None}
        self.api.make_request = Mock(return_value=json_data_book_found_edge_case)
        self.assertEqual(self.api.is_book_available(self.book), True)

    def test_books_by_author(self):
        json_data_book_not_found = None
        self.api.make_request = Mock(return_value=json_data_book_not_found)
        self.assertEqual(self.api.books_by_author(self.book_dne), [])

        request_url = "%s?author=%s" % (self.API_URL, self.author)
        self.api.make_request = Mock(return_value=self.books_by_author_response)
        self.assertEqual(self.api.books_by_author(self.author), self.books_by_author)
        self.api.make_request.assert_called_with(request_url)

    def test_get_book_info(self):
        json_data_book_not_found = None
        self.api.make_request = Mock(return_value=json_data_book_not_found)
        self.assertEqual(self.api.get_book_info(self.book_dne), [])

        request_url = "%s?q=%s" % (self.API_URL, self.book)
        self.api.make_request = Mock(return_value=self.book_found_json_data)
        self.assertEqual(self.api.get_book_info(self.book), self.books_data)
        self.api.make_request.assert_called_with(request_url)

    def test_get_ebooks(self):
        json_data_book_not_found = None
        self.api.make_request = Mock(return_value=json_data_book_not_found)
        self.assertEqual(self.api.get_ebooks(self.book_dne), [])

        request_url = "%s?q=%s" % (self.API_URL, self.e_book)
        self.api.make_request = Mock(return_value=self.e_book_payload_data)
        self.assertEqual(self.api.get_ebooks(self.e_book), self.e_books_data)
        self.api.make_request.assert_called_with(request_url)


if __name__ == "__main__":
    unittest.main()
