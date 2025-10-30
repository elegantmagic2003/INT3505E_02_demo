import connexion
from typing import Dict
from typing import Tuple
from typing import Union

from openapi_server.models.book import Book  # noqa: E501
from openapi_server.models.book_input import BookInput  # noqa: E501
from openapi_server.models.books_get200_response import BooksGet200Response  # noqa: E501
from openapi_server import util


def books_get(page=None, limit=None):  # noqa: E501
    """Lấy danh sách sách (có hỗ trợ phân trang)

     # noqa: E501

    :param page: Trang hiện tại (bắt đầu từ 1)
    :type page: int
    :param limit: Số lượng sách trên mỗi trang
    :type limit: int

    :rtype: Union[BooksGet200Response, Tuple[BooksGet200Response, int], Tuple[BooksGet200Response, int, Dict[str, str]]
    """
    return 'do some magic!'


def books_id_delete(id):  # noqa: E501
    """Xóa sách theo ID

     # noqa: E501

    :param id: 
    :type id: int

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return 'do some magic!'


def books_id_get(id):  # noqa: E501
    """Lấy thông tin chi tiết một sách

     # noqa: E501

    :param id: 
    :type id: int

    :rtype: Union[Book, Tuple[Book, int], Tuple[Book, int, Dict[str, str]]
    """
    return 'do some magic!'


def books_id_put(id, body):  # noqa: E501
    """Cập nhật thông tin sách

     # noqa: E501

    :param id: 
    :type id: int
    :param book_input: 
    :type book_input: dict | bytes

    :rtype: Union[Book, Tuple[Book, int], Tuple[Book, int, Dict[str, str]]
    """
    book_input = body
    if connexion.request.is_json:
        book_input = BookInput.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def books_post(body):  # noqa: E501
    """Thêm một sách mới

     # noqa: E501

    :param book_input: 
    :type book_input: dict | bytes

    :rtype: Union[Book, Tuple[Book, int], Tuple[Book, int, Dict[str, str]]
    """
    book_input = body
    if connexion.request.is_json:
        book_input = BookInput.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
