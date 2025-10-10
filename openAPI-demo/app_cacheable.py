from flask import Flask, jsonify, make_response
from models import db, Book

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books_cacheable.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/api/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    response = make_response(jsonify([b.to_dict() for b in books]))
    response.headers['Cache-Control'] = 'public, max-age=60'
    return response


@app.route('/api/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404

    response = make_response(jsonify(book.to_dict()))
    response.headers['Cache-Control'] = 'public, max-age=120'
    return response


if __name__ == '__main__':
    app.run(debug=True)
