from flask import Flask, request, jsonify
from models import db, Book, Borrow
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Khởi tạo DB lần đầu
with app.app_context():
    db.create_all()

# ---------------- Sách ----------------
@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    return jsonify([{"id": b.id, "title": b.title, "author": b.author, "available": b.available} for b in books])

@app.route('/books', methods=['POST'])
def add_book():
    data = request.json
    new_book = Book(title=data['title'], author=data['author'])
    db.session.add(new_book)
    db.session.commit()
    return jsonify({"message": "Book added!"}), 201

@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get_or_404(book_id)
    return jsonify({"id": book.id, "title": book.title, "author": book.author, "available": book.available})

@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": "Book deleted!"})

# ---------------- Mượn / Trả ----------------
@app.route('/borrow', methods=['POST'])
def borrow_book():
    data = request.json
    book = Book.query.get_or_404(data['book_id'])

    if not book.available:
        return jsonify({"error": "Book already borrowed"}), 400

    borrow = Borrow(user=data['user'], book=book)
    book.available = False
    db.session.add(borrow)
    db.session.commit()
    return jsonify({"message": "Book borrowed!"})

@app.route('/return/<int:borrow_id>', methods=['POST'])
def return_book(borrow_id):
    borrow = Borrow.query.get_or_404(borrow_id)
    if borrow.returned:
        return jsonify({"error": "Book already returned"}), 400

    borrow.returned = True
    borrow.book.available = True
    db.session.commit()
    return jsonify({"message": "Book returned!"})

if __name__ == '__main__':
    app.run(debug=True)
