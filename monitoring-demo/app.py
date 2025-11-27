from flask import Flask, request, jsonify, send_file
from flask_swagger_ui import get_swaggerui_blueprint
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from models import db, Book, User
import os
import logging
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_prometheus_metrics import register_metrics
from datetime import timedelta

# -------------------------
# App + Config
# -------------------------
app = Flask(__name__, static_folder="static", static_url_path="/static")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'dev-secret-key')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=2)

# Initialize extensions
db.init_app(app)
jwt = JWTManager(app)

# -------------------------
# Logging
# -------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

def audit_log(action, username, details=""):
    logging.info(f"[AUDIT] user={username} action={action} details={details}")

@app.before_request
def log_request():
    logging.info(f"{request.method} {request.path} from {request.remote_addr}")

# -------------------------
# Rate limiting
# -------------------------
limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=["200 per hour"]  # global default
)

# Example of more strict per-endpoint limiter can be used with decorator:
# @limiter.limit("10 per minute")

# -------------------------
# Prometheus metrics
# -------------------------
register_metrics(app, app_version="1.0.0", app_config="development")
# available at /metrics automatically by flask_prometheus_metrics

# -------------------------
# Swagger UI (static YAML)
# -------------------------
SWAGGER_URL = '/docs'
API_URL = '/static/book-api.yaml'  # create this file in static/
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL, API_URL,
    config={'app_name': "Book Management API"}
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# -------------------------
# Ensure DB exists
# -------------------------
with app.app_context():
    db.create_all()

# -------------------------
# Auth endpoints
# -------------------------
@app.route('/api/register', methods=['POST'])
@limiter.limit("5 per minute")
def register():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({"error": "username and password required"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 400

    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    logging.info(f"New user registered: {username}")
    return jsonify({"message": "User registered successfully"}), 201


@app.route('/api/login', methods=['POST'])
@limiter.limit("10 per minute")
def login():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({"error": "username and password required"}), 400

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        logging.warning(f"Failed login attempt for: {username}")
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(identity=user.username)
    logging.info(f"User logged in: {username}")
    return jsonify({"access_token": access_token})


# -------------------------
# CRUD endpoints (books)
# -------------------------
@app.route('/api/books', methods=['GET'])
@limiter.limit("30 per minute")
def get_books():
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 5, type=int)

    pagination = Book.query.paginate(page=page, per_page=limit, error_out=False)

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
@limiter.limit("60 per minute")
def get_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    return jsonify(book.to_dict())


@app.route('/api/books', methods=['POST'])
@jwt_required()
@limiter.limit("20 per minute")
def add_book():
    data = request.get_json() or {}
    title = data.get('title')
    author = data.get('author')
    if not title or not author:
        return jsonify({"error": "title and author required"}), 400

    book = Book(title=title, author=author, year=data.get('year'), genre=data.get('genre'))
    db.session.add(book)
    db.session.commit()

    current_user = get_jwt_identity()
    audit_log("ADD_BOOK", current_user, f"title={title}, id={book.id}")

    return jsonify(book.to_dict()), 201


@app.route('/api/books/<int:book_id>', methods=['PUT'])
@jwt_required()
@limiter.limit("20 per minute")
def update_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404

    data = request.get_json() or {}
    book.title = data.get('title', book.title)
    book.author = data.get('author', book.author)
    book.year = data.get('year', book.year)
    book.genre = data.get('genre', book.genre)
    db.session.commit()

    current_user = get_jwt_identity()
    audit_log("UPDATE_BOOK", current_user, f"id={book_id}")

    return jsonify(book.to_dict())


@app.route('/api/books/<int:book_id>', methods=['DELETE'])
@jwt_required()
@limiter.limit("10 per minute")
def delete_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404

    db.session.delete(book)
    db.session.commit()

    current_user = get_jwt_identity()
    audit_log("DELETE_BOOK", current_user, f"id={book_id}")

    return '', 204


# -------------------------
# Health check & static files (Swagger)
# -------------------------
@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"}), 200


# -------------------------
# Run
# -------------------------
if __name__ == '__main__':
    # In production use a WSGI server (gunicorn/uwsgi) and disable debug
    app.run(host="0.0.0.0", port=5000, debug=True)
