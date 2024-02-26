import os
from library import ext_api_interface
import json


def get_test_data_path():
    this_file = os.path.abspath(__file__)
    programs = os.path.dirname(this_file)
    app = os.path.dirname(programs)
    tests_data = os.path.join(app, 'tests_data')
    ext_api_interface_tests_data = os.path.join(tests_data, 'ext_api_interface')
    return ext_api_interface_tests_data


ext_api_interface_tests_data = get_test_data_path()


class ExtAPIIntGetData:
    def __init__(self):
        self.api = ext_api_interface.Books_API()

    def get_ebooks(self, book):
        print("get ebooks: " + book)
        ebooks = self.api.get_ebooks(book)
        print(ebooks)
        with open(os.path.join(ext_api_interface_tests_data, 'ebooks.txt'), 'w') as f:
            f.write(json.dumps(ebooks))

    def get_book_info(self, book):
        print("get book info: " + book)
        info = self.api.get_book_info(book)
        print(len(info))
        print(info)
        with open(os.path.join(ext_api_interface_tests_data, 'books.txt'), 'w') as f:
            f.write(json.dumps(info))

    def get_books_by_author(self, author):
        print("get books by author: " + author)
        books = self.api.books_by_author(author)
        print(len(books))
        print(books)
        with open(os.path.join(ext_api_interface_tests_data, 'books_by_author.txt'), 'w') as f:
            f.write(json.dumps(books))

    def get_books_by_author_response(self, author):
        print("get books by author: " + author)
        request_url = "%s?author=%s" % (self.api.API_URL, author)
        response = self.api.make_request(request_url)
        print(len(response))
        print(response)
        with open(os.path.join(ext_api_interface_tests_data, 'books_by_author_response.txt'), 'w') as f:
            f.write(json.dumps(response))

    def get_book_found_data(self, book, file_path):
        request_url = "%s?q=%s" % (self.api.API_URL, book)
        json_data = self.api.make_request(request_url)
        print(json_data)
        with open(os.path.join(ext_api_interface_tests_data, file_path), 'w') as f:
            f.write(json.dumps(json_data))


if __name__ == "__main__":
    getdata = ExtAPIIntGetData()
    getdata.get_ebooks('software architecture in practice')
    # getdata.get_ebooks('concurrency in go') # returns empty ebooks
    getdata.get_book_info('concurrency in go')
    getdata.get_books_by_author('Katherine Cox-Buday')
    getdata.get_books_by_author_response('Katherine Cox-Buday')
    getdata.get_book_found_data('concurrency in go', 'book_found_data.txt')
    getdata.get_book_found_data('software architecture in practice', 'book_found_ebook.txt')
