from flask import Flask, request, jsonify, make_response
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

        resp = make_response(jsonify({"message": "Đăng nhập thành công!"}))
        # Gửi token qua cookie
        resp.set_cookie('jwt', token, httponly=True, samesite='Lax')
        return resp
    else:
        return jsonify({"message": "Sai thông tin đăng nhập!"}), 401


@app.route('/protected')
def protected():
    token = request.cookies.get('jwt')
    if not token:
        return jsonify({"message": "Không có token trong cookie!"}), 401

    try:
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return jsonify({"message": f"Xin chào {data['user']}! Bạn đã truy cập thành công."})
    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token hết hạn!"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"message": "Token không hợp lệ!"}), 401


if __name__ == '__main__':
    app.run(debug=True, port=5003)
