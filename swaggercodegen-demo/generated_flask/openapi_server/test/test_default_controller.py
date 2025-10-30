import unittest

from flask import json

from openapi_server.models.book import Book  # noqa: E501
from openapi_server.models.book_input import BookInput  # noqa: E501
from openapi_server.models.books_get200_response import BooksGet200Response  # noqa: E501
from openapi_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_books_get(self):
        """Test case for books_get

        Lấy danh sách sách (có hỗ trợ phân trang)
        """
        query_string = [('page', 1),
                        ('limit', 5)]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/books',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_books_id_delete(self):
        """Test case for books_id_delete

        Xóa sách theo ID
        """
        headers = { 
        }
        response = self.client.open(
            '/api/books/{id}'.format(id=56),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_books_id_get(self):
        """Test case for books_id_get

        Lấy thông tin chi tiết một sách
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/books/{id}'.format(id=56),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_books_id_put(self):
        """Test case for books_id_put

        Cập nhật thông tin sách
        """
        book_input = {"year":0,"author":"author","genre":"genre","title":"title"}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/books/{id}'.format(id=56),
            method='PUT',
            headers=headers,
            data=json.dumps(book_input),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_books_post(self):
        """Test case for books_post

        Thêm một sách mới
        """
        book_input = {"year":0,"author":"author","genre":"genre","title":"title"}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/books',
            method='POST',
            headers=headers,
            data=json.dumps(book_input),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
