from flask import Flask, request, jsonify
import jwt, datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecret'

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    if data['username'] == 'kien' and data['password'] == '123':
        token = jwt.encode({
            'user': data['username'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }, app.config['SECRET_KEY'], algorithm='HS256')

        return jsonify({"token": token, "message": "Đăng nhập thành công!"})
    else:
        return jsonify({"message": "Sai thông tin đăng nhập!"}), 401


@app.route('/protected')
def protected():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({"message": "Thiếu token trong header!"}), 401

    try:
        token = auth_header.split(" ")[1]
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return jsonify({"message": f"Xin chào {data['user']}! Bạn đã truy cập thành công."})
    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token hết hạn!"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"message": "Token không hợp lệ!"}), 401


if __name__ == '__main__':
    app.run(debug=True, port=5002)
