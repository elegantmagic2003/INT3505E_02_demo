from flask import Flask, request, jsonify, send_file
from flask_swagger_ui import get_swaggerui_blueprint
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from models import db, Book, User
import os
app = Flask(__name__)

# --- Cấu hình SQLite ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'dev-secret-key')
db.init_app(app)

# --- Swagger UI ---
SWAGGER_URL = '/docs'
API_URL = '/static/book-api.yaml'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL, API_URL,
    config={'app_name': "Book Management API"}
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

with app.app_context():
    db.create_all()

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"error": "Username already exists"}), 400

    user = User(username=data['username'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201


@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if not user or not user.check_password(data['password']):
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(identity=user.username)
    return jsonify({"access_token": access_token})


# --- CRUD endpoints ---
@app.route('/api/books', methods=['GET'])
def get_books():
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 5, type=int)  # mặc định 5 sách mỗi trang

    # Query phân trang
    pagination = Book.query.paginate(page=page, per_page=limit, error_out=False)

    # Tạo response JSON
    response = {
        "page": pagination.page,
        "total_pages": pagination.pages,
        "total_items": pagination.total,
        "has_next": pagination.has_next,
        "has_prev": pagination.has_prev,
        "items": [book.to_dict() for book in pagination.items]
    }
    return jsonify(response)


@app.route('/api/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    return jsonify(book.to_dict())

@app.route('/api/books', methods=['POST'])
@jwt_required()
def add_book():
    data = request.get_json()
    book = Book(title=data['title'], author=data['author'], year=data.get('year'), genre=data.get('genre'))
    db.session.add(book)
    db.session.commit()
    return jsonify(book.to_dict()), 201

@app.route('/api/books/<int:book_id>', methods=['PUT'])
@jwt_required()
def update_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404

    data = request.get_json()
    book.title = data.get('title', book.title)
    book.author = data.get('author', book.author)
    book.year = data.get('year', book.year)
    book.genre = data.get('genre', book.genre)
    db.session.commit()
    return jsonify(book.to_dict())

@app.route('/api/books/<int:book_id>', methods=['DELETE'])
@jwt_required()
def delete_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404

    db.session.delete(book)
    db.session.commit()
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
